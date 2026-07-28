variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "fraud-detection"
}

variable "unique_suffix" {
  type = string
}

variable "enable_streaming" {
  type    = bool
  default = false
}

variable "kinesis_shard_count" {
  type    = number
  default = 1
}

variable "bucket_versioning_enabled" {
  type    = bool
  default = true
}

variable "allow_bucket_force_destroy" {
  type    = bool
  default = false
}

variable "log_retention_days" {
  type    = number
  default = 14
}

variable "tags" {
  type    = map(string)
  default = {}
}
