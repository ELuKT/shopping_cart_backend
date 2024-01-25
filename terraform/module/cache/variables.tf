variable "project_name" {
  description = "project name"
  type = string
  default = "example"
}

variable "region" {
  description = "aws region"
  type = string
  default = "ap-northeast-1"
}

variable "rediscloud_api_key" {
  description = "rediscloud api key"
  type = string
}

variable "rediscloud_secret_key" {
  description = "rediscloud secret key"
  type = string
}