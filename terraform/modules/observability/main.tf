resource "aws_cloudwatch_log_group" "pipeline" {
  name              = "/aws/fraud-detection/${var.name_prefix}"
  retention_in_days = var.log_retention_days
  tags              = var.tags
}
