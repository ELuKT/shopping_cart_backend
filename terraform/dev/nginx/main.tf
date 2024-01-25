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
      name = "nginx"
    }
  }
}

provider "aws" {
  region = var.region
}

resource "aws_ecs_service" "nginx_es" {
  name            = "${var.project_name}-nginx"
  cluster         = var.aws_ecs_cluster_id
  task_definition = aws_ecs_task_definition.nginx_td.arn
  desired_count   = 1
  launch_type = "FARGATE"
  enable_ecs_managed_tags = true
  wait_for_steady_state = true
  network_configuration {
    subnets = var.aws_public_subnets_ids
    assign_public_ip = true
    security_groups = [aws_security_group.nginx_sg.id]
  }
}

resource "aws_security_group" "nginx_sg" {
  name        = "nginx-sg"
  vpc_id      = var.aws_vpc_id

  ingress {
    description      = "custom envoy sidecar port"
    from_port        = 19001
    to_port          = 19001
    protocol         = "tcp"
    cidr_blocks      = [var.aws_vpc_cidr_block]
  }

  ingress {
    description      = "http port"
    from_port        = 80
    to_port          = 80
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

resource "aws_ecs_task_definition" "nginx_td" {
  
  family = "${var.project_name}-nginx"
  execution_role_arn = var.aws_iam_role_arn
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 256
  memory                   = 512
  container_definitions = jsonencode([
    {
      name      = "${var.project_name}-nginx"
      image     = "${var.aws_account}.dkr.ecr.${var.region}.amazonaws.com/aws-nginx:0.1.0"
      cpu       = 0
      logConfiguration= {
          logDriver= "awslogs",
          options= {
              awslogs-group=  "${var.project_name}-lg",
              awslogs-region= "${var.region}",
              awslogs-stream-prefix= "${var.project_name}"
          }
      }
      healthCheck = {
        Command= [
            "CMD-SHELL", 
            "curl -f http://localhost/health || exit 1"
        ]
        Interval= 5
        Timeout= 2
        Retries= 3
      }
    },
    {
      name      = "${var.project_name}-envoy-consul"
      image     = "${var.aws_account}.dkr.ecr.${var.region}.amazonaws.com/aws-consul-envoy:0.1.0"
      cpu       = 0
      command = ["consul", "connect", "envoy", "-sidecar-for", "nginx"]
      dependsOn = [
        {
          condition = "HEALTHY",
          containerName = "${var.project_name}-nginx"
        }
      ]
      environment= [
          {
              name= "CONSUL_HTTP_ADDR",
              value= "${var.aws_consul_server_private_ip}:8500"
          },
          {
              name= "CONSUL_GRPC_ADDR",
              value= "${var.aws_consul_server_private_ip}:8502"
          },
          {
              name= "SERVICE_CONFIG",
              value= "/consul/config/nginx.json"
          },
          {
              name= "APP_NAME",
              value= "nginx"
          },
          {
              name= "APP_PORT",
              value= "80"
          },
          {
              name= "SERVICE_NAME",
              value= "nginx"
          },
          {
              name= "UPSTREAM_SERVICE_NAME",
              value= "fastapi-sc-backend"
          },
          {
              name= "UPSTREAM_BIND_PORT",
              value= "8001"
          },
          {
              name= "NODE_NAME",
              value= "nginx"
          }
      ],
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

data "aws_network_interface" "nginx_es_interface" {
  depends_on = [aws_ecs_service.nginx_es]
  filter {
    name   = "tag:aws:ecs:serviceName"
    values = ["${var.project_name}-nginx"]
  }
}
