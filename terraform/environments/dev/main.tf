module "dev" {
  source = "../.."

  aws_region                   = var.aws_region
  project_name                 = var.project_name
  environment                  = "dev"
  unique_suffix                = var.unique_suffix
  enable_streaming             = var.enable_streaming
  kinesis_shard_count          = var.kinesis_shard_count
  bucket_versioning_enabled    = var.bucket_versioning_enabled
  allow_bucket_force_destroy   = var.allow_bucket_force_destroy
  log_retention_days           = var.log_retention_days
  tags                         = var.tags
}
