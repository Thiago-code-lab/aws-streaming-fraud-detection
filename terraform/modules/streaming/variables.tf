variable "name_prefix" {
  type = string
}

variable "kinesis_shard_count" {
  type = number
}

variable "tags" {
  type = map(string)
}
