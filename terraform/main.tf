module "storage" {
  source = "./modules/storage"

  name_prefix                   = local.name_prefix
  bucket_versioning_enabled     = var.bucket_versioning_enabled
  allow_bucket_force_destroy    = var.allow_bucket_force_destroy
  noncurrent_version_expiration = 30
  tags                          = local.common_tags
}

module "streaming" {
  source = "./modules/streaming"
  count  = var.enable_streaming ? 1 : 0

  name_prefix         = local.name_prefix
  kinesis_shard_count = var.kinesis_shard_count
  tags                = local.common_tags
}

module "catalog" {
  source = "./modules/catalog"

  database_name       = replace("${var.project_name}_${var.environment}", "-", "_")
  processed_bucket_id = module.storage.processed_bucket_id
  table_name          = "fraud_assessments"
}

module "processing" {
  source = "./modules/processing"

  name_prefix          = local.name_prefix
  raw_bucket_arn       = module.storage.raw_bucket_arn
  processed_bucket_arn = module.storage.processed_bucket_arn
  tags                 = local.common_tags
}

module "observability" {
  source = "./modules/observability"

  name_prefix        = local.name_prefix
  log_retention_days = var.log_retention_days
  tags               = local.common_tags
}
