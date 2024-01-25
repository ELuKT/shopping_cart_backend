output "aws_vpc_id" {
  value = aws_vpc.vpc.id
}

output "cidr_block" {
  value = aws_vpc.vpc.cidr_block
}

output "private_subnets_ids" {
  value = [for subnet in aws_subnet.private_subnet : subnet.id]
}

output "public_subnets_ids" {
  value = [for subnet in aws_subnet.public_subnet : subnet.id]
}

output "nat_gateway_ip" {
  value = aws_nat_gateway.nat_gateway.public_ip
}

output "aws_ecs_cluster_id" {
  value = aws_ecs_cluster.ecs_cluster.id
}

output "aws_iam_role_arn" {
  value = aws_iam_role.task_exection_role.arn
}

output "aws_consul_server_private_ip" {
  value = data.aws_network_interface.consul_server_interface.private_ip
}

output "aws_consul_server_private_ips" {
  value = data.aws_network_interface.consul_server_interface.private_ips
}
