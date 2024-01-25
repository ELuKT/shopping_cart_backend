#!/bin/bash
export TF_CLI_CONFIG_FILE="../.terraformrc"

cd infra
aws_private_subnets_ids=$(terraform output aws_private_subnets_ids)
aws_vpc_id=$(terraform output -raw aws_vpc_id)
aws_vpc_cidr_block=$(terraform output -raw aws_vpc_cidr_block)
aws_iam_role_arn=$(terraform output -raw aws_iam_role_arn)
aws_ecs_cluster_id=$(terraform output -raw aws_ecs_cluster_id)
aws_consul_server_private_ip=$(terraform output -raw aws_consul_server_private_ip)

cd ../app
terraform init
terraform apply -var-file="../general.tfvars" \
    -var="aws_private_subnets_ids=$aws_private_subnets_ids" \
    -var="aws_vpc_id=$aws_vpc_id" \
    -var="aws_vpc_cidr_block=$aws_vpc_cidr_block" \
    -var="aws_iam_role_arn=$aws_iam_role_arn" \
    -var="aws_ecs_cluster_id=$aws_ecs_cluster_id" \
    -var="aws_consul_server_private_ip=$aws_consul_server_private_ip" \
    -auto-approve