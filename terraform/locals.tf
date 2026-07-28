locals {
  name_prefix = "${var.project_name}-${var.environment}-${var.unique_suffix}"
  common_tags = merge(
    {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "Terraform"
      Repository  = "aws-streaming-fraud-detection"
    },
    var.tags,
  )
}
