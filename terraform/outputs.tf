/*
output "kinesis_stream_name" {
  value       = aws_kinesis_stream.transaction_stream.name
  description = "Nome do Stream para configurar no script Python"
}
*/

output "raw_bucket_name" {
  value       = aws_s3_bucket.raw_bucket.bucket
  description = "Nome do Bucket Raw"
}