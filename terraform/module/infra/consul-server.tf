resource "aws_ecs_service" "consul_server_es" {
  name            = "${var.project_name}-consul-server"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.consul_server_td.arn
  desired_count   = 1
  launch_type = "FARGATE"
  enable_ecs_managed_tags = true # to be able to get ip from server task
  wait_for_steady_state = true
  network_configuration {
    subnets = [for subnet in aws_subnet.private_subnet : subnet.id]
    security_groups = [aws_security_group.consul_server_sg.id]
  }
}

resource "aws_security_group" "consul_server_sg" {
  name        = "consul-server-sg"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    description      = "port for handling incoming requests from other agents"
    from_port        = 8300
    to_port          = 8300
    protocol         = "tcp"
    cidr_blocks      = [aws_vpc.vpc.cidr_block]
  }

  ingress {
    description      = "Currently gRPC is only used to expose the xDS API to Envoy proxies."
    from_port        = 8502
    to_port          = 8502
    protocol         = "tcp"
    cidr_blocks      = [aws_vpc.vpc.cidr_block]
  }

  ingress {
    description      = "ui/api port"
    from_port        = 8500
    to_port          = 8500
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_task_definition" "consul_server_td" {
  family = "${var.project_name}-consul-server"
  execution_role_arn = aws_iam_role.task_exection_role.arn
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  container_definitions = jsonencode([
    {
      name      = "${var.project_name}-consul-server"
      image     = "hashicorp/consul:1.16.2"
      cpu       = 0
      # https://developer.hashicorp.com/consul/docs/agent/config/cli-flags#_bind
      # https://developer.hashicorp.com/consul/docs/agent/config/cli-flags#ui-content-path use "consul-server" path in nginx config
      command = ["agent", "-server", "-bootstrap-expect=1", "-ui", "-client=0.0.0.0", "-bind={{ GetPrivateInterfaces | include \"network\" \"${aws_vpc.vpc.cidr_block}\" | attr \"address\" }}", "-grpc-port=8502", "-ui-content-path=consul-server"]
      logConfiguration= {
          logDriver= "awslogs",
          options= {
              awslogs-group=  "${var.project_name}-lg",
              awslogs-region= "${var.region}",
              awslogs-stream-prefix= "${var.project_name}"
          }
      }
    }
  ])
}

data "aws_network_interface" "consul_server_interface" {
  depends_on = [aws_ecs_service.consul_server_es]
  filter {
    name   = "tag:aws:ecs:serviceName"
    values = ["${var.project_name}-consul-server"]
  }
}

