variable "aws_region" {
  description = "AWS region used by the educational environment."
  type        = string
  default     = "us-east-1"

  validation {
    condition     = contains(["us-east-1", "us-east-2", "us-west-2", "sa-east-1"], var.aws_region)
    error_message = "Use a region supported by the project examples."
  }
}

variable "project_name" {
  description = "Short project identifier used in resource names."
  type        = string
  default     = "fraud-detection"

  validation {
    condition     = can(regex("^[a-z0-9-]{3,32}$", var.project_name))
    error_message = "project_name must contain 3 to 32 lowercase letters, numbers or hyphens."
  }
}

variable "environment" {
  description = "Environment name."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging or prod."
  }
}

variable "unique_suffix" {
  description = "Non-secret suffix used to keep globally unique bucket names."
  type        = string

  validation {
    condition     = can(regex("^[a-z0-9-]{4,20}$", var.unique_suffix))
    error_message = "unique_suffix must contain 4 to 20 lowercase letters, numbers or hyphens."
  }
}

variable "enable_streaming" {
  description = "Creates Kinesis and Lambda resources when true. Disabled by default to avoid recurring costs."
  type        = bool
  default     = false
}

variable "kinesis_shard_count" {
  description = "Provisioned shard count for the optional Kinesis stream."
  type        = number
  default     = 1

  validation {
    condition     = var.kinesis_shard_count >= 1 && var.kinesis_shard_count <= 2
    error_message = "Use 1 or 2 shards for the educational low-cost environment."
  }
}

variable "bucket_versioning_enabled" {
  description = "Enables S3 bucket versioning."
  type        = bool
  default     = true
}

variable "allow_bucket_force_destroy" {
  description = "Allows deleting non-empty buckets. Keep false except for disposable labs."
  type        = bool
  default     = false
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days."
  type        = number
  default     = 14
}

variable "tags" {
  description = "Additional tags applied to resources."
  type        = map(string)
  default     = {}
}
