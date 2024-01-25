# Terraform 0.12 and later intentionally track only root module outputs in the state. 
# To expose module outputs for external consumption, you must export them from the root module using an output block

output "mongo_atlas_endpoint" {
  value = module.fastapi-sc-dev-db.mongodb_endpoint
}

output "aws_private_subnets_ids" {
  value = module.fastapi-sc-dev-infra.private_subnets_ids
}

output "aws_public_subnets_ids" {
  value = module.fastapi-sc-dev-infra.public_subnets_ids
}

output "aws_vpc_id" {
  value = module.fastapi-sc-dev-infra.aws_vpc_id
}

output "aws_vpc_cidr_block" {
  value = module.fastapi-sc-dev-infra.cidr_block
}

output "aws_consul_server_private_ip" {
  value = module.fastapi-sc-dev-infra.aws_consul_server_private_ip
}

output "aws_consul_server_private_ips" {
  value = module.fastapi-sc-dev-infra.aws_consul_server_private_ips
}

output "aws_ecs_cluster_id" {
  value = module.fastapi-sc-dev-infra.aws_ecs_cluster_id
}

output "aws_iam_role_arn" {
  value = module.fastapi-sc-dev-infra.aws_iam_role_arn
}
