resource "aws_glue_catalog_database" "fraud" {
  name = var.database_name
}

resource "aws_glue_catalog_table" "fraud_assessments" {
  database_name = aws_glue_catalog_database.fraud.name
  name          = var.table_name
  table_type    = "EXTERNAL_TABLE"

  parameters = {
    classification = "parquet"
  }

  partition_keys {
    name = "year"
    type = "string"
  }

  partition_keys {
    name = "month"
    type = "string"
  }

  partition_keys {
    name = "day"
    type = "string"
  }

  partition_keys {
    name = "hour"
    type = "string"
  }

  storage_descriptor {
    location      = "s3://${var.processed_bucket_id}/fraud_assessments/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }

    columns {
      name = "transaction_id"
      type = "string"
    }
    columns {
      name = "event_timestamp"
      type = "timestamp"
    }
    columns {
      name = "processed_at"
      type = "timestamp"
    }
    columns {
      name = "amount"
      type = "double"
    }
    columns {
      name = "state"
      type = "string"
    }
    columns {
      name = "device_type"
      type = "string"
    }
    columns {
      name = "risk_score"
      type = "int"
    }
    columns {
      name = "risk_level"
      type = "string"
    }
    columns {
      name = "triggered_rules"
      type = "array<string>"
    }
    columns {
      name = "rules_version"
      type = "string"
    }
    columns {
      name = "customer_id"
      type = "string"
    }
    columns {
      name = "masked_card"
      type = "string"
    }
    columns {
      name = "merchant_category"
      type = "string"
    }
  }
}
