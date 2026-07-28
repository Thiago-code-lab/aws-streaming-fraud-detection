resource "aws_kinesis_stream" "transactions" {
  name             = "${var.name_prefix}-transactions"
  shard_count      = var.kinesis_shard_count
  retention_period = 24

  stream_mode_details {
    stream_mode = "PROVISIONED"
  }

  encryption_type = "KMS"
  kms_key_id      = "alias/aws/kinesis"
  tags            = var.tags
}
