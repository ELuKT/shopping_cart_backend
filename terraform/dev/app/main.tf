terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
      # ~> Allows only the rightmost version component to increment. This is usually called the pessimistic constraint operator.
      # ~> 5.0 equals 5.1 ~ 5.x
      # ~> 5.0.0 equals 5.0.1 ~ 5.0.x
    }
  }

  cloud {
    # Variables may not be used here.
    organization = "buseric"

    workspaces {
      # Variables may not be used here.
      name = "app"
    }
  }
}

provider "aws" {
  region = var.region
}

locals {
  env_name = terraform.workspace
}

module "fastapi-sc-dev-service-env" {
  source = "../../module/service_env"

  project_name = var.project_name
  region = var.region
}

module "fastapi-sc-dev-service" {
  source = "../../module/service"

  project_name = var.project_name
  region = var.region
  aws_account = var.aws_account
  aws_private_subnets_ids = var.aws_private_subnets_ids
  aws_vpc_id = var.aws_vpc_id
  aws_vpc_cidr_block = var.aws_vpc_cidr_block
  aws_ecs_cluster_id = var.aws_ecs_cluster_id
  aws_iam_role_arn = var.aws_iam_role_arn
  aws_consul_server_private_ip = var.aws_consul_server_private_ip
}