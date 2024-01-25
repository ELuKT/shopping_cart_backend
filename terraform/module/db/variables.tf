variable "project_name" {
  description = "project name"
  type = string
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

variable "aws_nat_gateway_ip" {
  description = "aws nat gateway ip"
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
