output "raw_bucket_name" {
  description = "Raw S3 bucket for JSON transaction events."
  value       = module.storage.raw_bucket_id
}

output "processed_bucket_name" {
  description = "Processed S3 bucket for fraud assessments in Parquet."
  value       = module.storage.processed_bucket_id
}

output "glue_database_name" {
  description = "Glue database used by Athena."
  value       = module.catalog.database_name
}

output "kinesis_stream_name" {
  description = "Optional Kinesis stream name. Null when streaming is disabled."
  value       = var.enable_streaming ? module.streaming[0].stream_name : null
}
