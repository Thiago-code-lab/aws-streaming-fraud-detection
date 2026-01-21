#!/usr/bin/env python3
"""
Fraud Detection Spark Job for AWS Glue

This script processes streaming transaction data from Kinesis and applies
fraud detection algorithms to identify suspicious transactions.
"""

import sys
import json
from datetime import datetime, timedelta
from pyspark.context import SparkContext
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType, TimestampType
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame

class FraudDetector:
    def __init__(self, spark, glue_context):
        """
        Initialize the fraud detector.
        
        Args:
            spark: SparkSession
            glue_context: GlueContext
        """
        self.spark = spark
        self.glue_context = glue_context
        
        # Define schema for transaction data
        self.transaction_schema = StructType([
            StructField("transaction_id", StringType(), True),
            StructField("user_id", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("amount", DoubleType(), True),
            StructField("currency", StringType(), True),
            StructField("merchant", StringType(), True),
            StructField("category", StringType(), True),
            StructField("country", StringType(), True),
            StructField("ip_address", StringType(), True),
            StructField("device_id", StringType(), True),
            StructField("is_fraudulent", BooleanType(), True)
        ])
    
    def detect_amount_anomalies(self, df):
        """
        Detect transactions with unusually high amounts.
        
        Args:
            df: DataFrame with transaction data
            
        Returns:
            DataFrame with fraud indicators
        """
        # Calculate user-specific amount statistics
        user_stats = df.groupBy("user_id").agg(
            F.mean("amount").alias("avg_amount"),
            F.stddev("amount").alias("std_amount"),
            F.count("*").alias("transaction_count")
        )
        
        # Join with original data and calculate z-score
        df_with_stats = df.join(user_stats, "user_id", "left")
        
        # Flag transactions with amount > 3 standard deviations from user average
        df_with_fraud_flags = df_with_stats.withColumn(
            "amount_anomaly",
            F.when(
                (F.col("amount") > (F.col("avg_amount") + 3 * F.col("std_amount"))) &
                (F.col("transaction_count") > 5),  # Only for users with sufficient history
                1
            ).otherwise(0)
        )
        
        return df_with_fraud_flags
    
    def detect_velocity_anomalies(self, df):
        """
        Detect high-frequency transactions (velocity fraud).
        
        Args:
            df: DataFrame with transaction data
            
        Returns:
            DataFrame with velocity fraud indicators
        """
        # Window specification for time-based analysis
        window_spec = F.window(
            F.col("timestamp"), "5 minutes", "1 minute"
        )
        
        # Count transactions per user in 5-minute windows
        transaction_counts = df.groupBy(
            "user_id", window_spec
        ).count().withColumnRenamed("count", "tx_count_5min")
        
        # Flag users with > 10 transactions in 5 minutes
        velocity_fraud = transaction_counts.filter(
            F.col("tx_count_5min") > 10
        ).select("user_id", "window.start", "window.end")
        
        return velocity_fraud
    
    def detect_location_anomalies(self, df):
        """
        Detect transactions from unusual locations.
        
        Args:
            df: DataFrame with transaction data
            
        Returns:
            DataFrame with location fraud indicators
        """
        # Get user's typical countries
        user_countries = df.groupBy("user_id").agg(
            F.collect_set("country").alias("user_countries")
        )
        
        # Join and flag transactions from new countries
        df_with_countries = df.join(user_countries, "user_id", "left")
        
        df_with_location_flags = df_with_countries.withColumn(
            "location_anomaly",
            F.when(
                ~F.array_contains(F.col("user_countries"), F.col("country")),
                1
            ).otherwise(0)
        )
        
        return df_with_location_flags
    
    def calculate_fraud_score(self, df):
        """
        Calculate overall fraud score based on various indicators.
        
        Args:
            df: DataFrame with fraud indicators
            
        Returns:
            DataFrame with final fraud scores
        """
        # Combine different fraud indicators
        df_with_score = df.withColumn(
            "fraud_score",
            F.col("amount_anomaly") * 0.4 + 
            F.col("location_anomaly") * 0.3 +
            F.when(F.col("is_fraudulent") == True, 0.3).otherwise(0)
        )
        
        # Add risk level classification
        df_with_risk = df_with_score.withColumn(
            "risk_level",
            F.when(F.col("fraud_score") >= 0.7, "HIGH")
            .when(F.col("fraud_score") >= 0.4, "MEDIUM")
            .otherwise("LOW")
        )
        
        return df_with_risk
    
    def process_transactions(self, kinesis_stream_name):
        """
        Main processing function for streaming transactions.
        
        Args:
            kinesis_stream_name (str): Name of the Kinesis stream
        """
        # Read from Kinesis stream
        df = self.spark.readStream \
            .format("kinesis") \
            .option("streamName", kinesis_stream_name) \
            .option("startingposition", "TRIM_HORIZON") \
            .load()
        
        # Parse JSON data
        parsed_df = df.selectExpr("CAST(data AS STRING) as json_data") \
            .select(F.from_json("json_data", self.transaction_schema).alias("data")) \
            .select("data.*")
        
        # Convert timestamp string to timestamp type
        parsed_df = parsed_df.withColumn(
            "timestamp",
            F.to_timestamp("timestamp")
        )
        
        # Apply fraud detection algorithms
        df_with_amount_anomalies = self.detect_amount_anomalies(parsed_df)
        df_with_location_anomalies = self.detect_location_anomalies(df_with_amount_anomalies)
        df_final = self.calculate_fraud_score(df_with_location_anomalies)
        
        # Select relevant columns for output
        output_df = df_final.select(
            "transaction_id",
            "user_id",
            "timestamp",
            "amount",
            "merchant",
            "country",
            "fraud_score",
            "risk_level",
            "is_fraudulent"
        )
        
        # Write high-risk transactions to separate stream/alert
        high_risk_df = output_df.filter(F.col("risk_level") == "HIGH")
        
        # Console output for monitoring
        console_query = output_df.writeStream \
            .outputMode("append") \
            .format("console") \
            .option("truncate", "false") \
            .start()
        
        # Write high-risk transactions to S3
        if not high_risk_df.rdd.isEmpty():
            s3_query = high_risk_df.writeStream \
                .outputMode("append") \
                .format("parquet") \
                .option("path", "s3://fraud-detection-processed-data/high-risk/") \
                .option("checkpointLocation", "s3://fraud-detection-processed-data/checkpoints/high-risk/") \
                .start()
        
        # Wait for streams to finish
        console_query.awaitTermination()

def main():
    """Main function to run the fraud detection job."""
    # Get job parameters
    args = getResolvedOptions(sys.argv, ['JOB_NAME', 'KINESIS_STREAM_NAME'])
    
    # Initialize Spark and Glue contexts
    sc = SparkContext()
    glue_context = GlueContext(sc)
    spark = glue_context.spark_session
    
    # Create fraud detector and run processing
    detector = FraudDetector(spark, glue_context)
    detector.process_transactions(args['KINESIS_STREAM_NAME'])

if __name__ == "__main__":
    main()
