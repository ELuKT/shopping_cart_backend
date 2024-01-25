resource "aws_ecs_service" "ecs_service" {
  name            = "${var.project_name}-es"
  cluster         = var.aws_ecs_cluster_id
  task_definition = aws_ecs_task_definition.task_definition.arn
  desired_count   = 1
  launch_type = "FARGATE"

  # Placement strategies are not supported with FARGATE launch type.
  # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-placement.html
  # ordered_placement_strategy {}

  # Network Configuration must be provided when networkMode 'awsvpc' is specified.
  network_configuration {
    subnets = var.aws_private_subnets_ids
    security_groups = [aws_security_group.app_sg.id]
  }
}

resource "aws_security_group" "app_sg" {
  name        = "app-sg"
  vpc_id      = var.aws_vpc_id

  ingress {
    description      = "custom envoy sidecar port"
    from_port        = 19001
    to_port          = 19001
    protocol         = "tcp"
    cidr_blocks      = [var.aws_vpc_cidr_block]
  }

  ingress {
    description      = "app port"
    from_port        = 8000
    to_port          = 8000
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

# For using s3 env, must have below settings: 
# if task is in public subnet, vpc must have internet gateway and aws_ecs_service.network_configuration.assign_public_ip must be true and 
# if task is in private subnet, your must set up NAT gateway
# https://www.youtube.com/watch?v=AyFiJqoulpY using vpc endpoint to saving cost
resource "aws_ecs_task_definition" "task_definition" {
  family = "${var.project_name}-td"
  execution_role_arn = var.aws_iam_role_arn # the container agent to make AWS API requests
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  # https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-cpu-memory-error.html
  cpu                      = 256 #  If the requires_compatibilities is FARGATE this field is required
  memory                   = 512 #  If the requires_compatibilities is FARGATE this field is required
  container_definitions = jsonencode([
    {
      name      = "${var.project_name}"
      image     = "${var.aws_account}.dkr.ecr.${var.region}.amazonaws.com/${var.project_name}:0.1.0"
      cpu       = 0 
      environmentFiles= [
          {
              value= "arn:aws:s3:::${var.project_name}-env/dev.env",
              type= "s3"
          },
          {
              value= "arn:aws:s3:::${var.project_name}-env/mongo_atlas_endpoint.env",
              type= "s3"
          }
      ],
      logConfiguration= {
          logDriver= "awslogs",
          options= {
              awslogs-group=  "${var.project_name}-lg",
              awslogs-region= "${var.region}",
              awslogs-stream-prefix= "${var.project_name}" # Optional for the EC2 launch type, required for the Fargate launch type
          }
      }
      # curl must be installed in the image
      healthCheck = {
        Command= [
            "CMD-SHELL", 
            "curl -f http://localhost:8000/v1/health/ || exit 1"
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
      command = ["consul", "connect", "envoy", "-sidecar-for", "fastapi-sc-backend-1"]
      dependsOn = [
        {
          condition = "HEALTHY",
          containerName = "${var.project_name}"
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
              value= "/consul/config/fastapi-sc-backend-1.json"
          },
          {
              name= "APP_NAME",
              value= "fastapi-sc-backend-1"
          },
          {
              name= "APP_PORT",
              value= "8000"
          },
          {
              name= "SERVICE_NAME",
              value= "fastapi-sc-backend"
          },
          {
              name= "NODE_NAME",
              value= "fastapi-sc-backend"
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
  # here document example
  # container_definitions = <<TASK_DEFINITION
  # [
  #   {
  #     "name"      : "${var.project_name}"
  #     ...
  #             "awslogs-stream-prefix": "${var.project_name}"
  #         }
  #     }
  #   }
  # ]
  # TASK_DEFINITION
}
