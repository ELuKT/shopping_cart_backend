output "aws_nginx_public_ip" {
    value = data.aws_network_interface.nginx_es_interface.association[0].public_ip
}

output "aws_nginx_public_dns" {
    value = data.aws_network_interface.nginx_es_interface.association[0].public_dns_name
}
