resource "aws_cloudwatch_log_group" "log_group" {
  name = "${var.project_name}-lg"
}

resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.project_name}-cluster"

  configuration {
    execute_command_configuration {
      logging = "OVERRIDE"
      log_configuration {
        cloud_watch_log_group_name = aws_cloudwatch_log_group.log_group.name
      }
    }
  }

  
  tags = {
    Name = "${var.project_name}-ecs"
  }
}

# aws console create cluster will give you FARGATE_SPOT and FARGATE provider automatically
resource "aws_ecs_cluster_capacity_providers" "cluster_capacity_providers" {
  cluster_name = aws_ecs_cluster.ecs_cluster.name

  capacity_providers = ["FARGATE_SPOT"]
}