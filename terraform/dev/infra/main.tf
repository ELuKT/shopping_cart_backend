terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  cloud {
    organization = "buseric"

    workspaces {
      name = "infra"
    }
  }
}

provider "aws" {
  region = var.region
}

locals {
  env_name = terraform.workspace
}

module "fastapi-sc-dev-infra" {
  source = "../../module/infra"

  project_name = var.project_name
}

module "fastapi-sc-dev-db" {
  # https://github.com/hashicorp/terraform/issues/1439
  # hard code source seems inevitable
  source = "../../module/db"

  project_name = var.project_name
  mongodbatlas_public_key = var.mongodbatlas_public_key
  mongodbatlas_private_key = var.mongodbatlas_private_key
  mongodbatlas_org_id = var.mongodbatlas_org_id
  mongodbatlas_database_username = var.mongodbatlas_database_username
  mongodbatlas_database_password = var.mongodbatlas_database_password
  mongodbatlas_database_name = var.mongodbatlas_database_name
  aws_nat_gateway_ip = module.fastapi-sc-dev-infra.nat_gateway_ip
}
