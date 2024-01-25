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

variable "aws_account" {
  description = "aws account"
  type = string
  sensitive = true
}

variable "aws_private_subnets_ids" {
  description = "aws private subnets arns"
  type = list
}

variable "aws_vpc_id" {
  type = string
}

variable "aws_vpc_cidr_block" {
  type = string
}

variable "aws_iam_role_arn" {
  type = string
}

variable "aws_ecs_cluster_id" {
  type = string
}

variable "aws_consul_server_private_ip" {
  type = string
}
