output "stream_name" {
  value = aws_kinesis_stream.transactions.name
}

output "stream_arn" {
  value = aws_kinesis_stream.transactions.arn
}
