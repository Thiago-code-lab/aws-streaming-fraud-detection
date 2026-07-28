output "raw_bucket_name" {
  value = module.dev.raw_bucket_name
}

output "processed_bucket_name" {
  value = module.dev.processed_bucket_name
}

output "glue_database_name" {
  value = module.dev.glue_database_name
}

output "kinesis_stream_name" {
  value = module.dev.kinesis_stream_name
}
