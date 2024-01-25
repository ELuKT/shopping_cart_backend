data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "task_exection_role" {
  name               = "${var.project_name}-task-exection-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy" "AmazonECSTaskExecutionRolePolicy" {
  arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy_attachment" "policy_attachment" {
  role       = aws_iam_role.task_exection_role.name
  policy_arn = data.aws_iam_policy.AmazonECSTaskExecutionRolePolicy.arn
}

resource "aws_iam_role_policy_attachment" "policy_attachment_2" {
  role       = aws_iam_role.task_exection_role.name
  policy_arn = aws_iam_policy.env_policy.arn
}

data "aws_iam_policy_document" "policy_document" {
  statement {
    effect    = "Allow"
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::${var.project_name}-env/*"]
  }

  statement {
    effect    = "Allow"
    actions   = ["s3:GetBucketLocation"]
    resources = ["arn:aws:s3:::${var.project_name}-env"]
  }
}

resource "aws_iam_policy" "env_policy" {
  name        = "${var.project_name}-ecs-env-policy"
  description = "let ecs get env file from s3"
  policy      = data.aws_iam_policy_document.policy_document.json
}
