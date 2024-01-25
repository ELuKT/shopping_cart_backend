variable "project_name" {
  description = "project name"
  type = string
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

variable "mongodbatlas_public_key" {
  description = "mongodbatlas public key"
  type = string
  sensitive = true
}

variable "mongodbatlas_private_key" {
  description = "mongodbatlas private key"
  type = string
  sensitive = true
}

variable "mongodbatlas_org_id" {
  description = "mongodbatlas organization id"
  type = string
  sensitive = true
}

variable "mongodbatlas_database_username" {
  description = "mongodbatlas database username"
  type = string
  sensitive = true
}

variable "mongodbatlas_database_password" {
  description = "mongodbatlas database password"
  type = string
  sensitive = true
}

variable "mongodbatlas_database_name" {
  description = "mongodbatlas database name"
  type = string
  sensitive = true
}
