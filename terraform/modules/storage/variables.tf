variable "name_prefix" {
  type = string
}

variable "bucket_versioning_enabled" {
  type = bool
}

variable "allow_bucket_force_destroy" {
  type = bool
}

variable "noncurrent_version_expiration" {
  type = number
}

variable "tags" {
  type = map(string)
}
