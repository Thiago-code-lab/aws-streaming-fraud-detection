variable "name_prefix" {
  type = string
}

variable "log_retention_days" {
  type = number
}

variable "tags" {
  type = map(string)
}
