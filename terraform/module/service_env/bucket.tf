
# we execute apply command in dev/app folder and dev.env is in dev
locals {
  env_file = "../dev.env"
  mongo_atlas_endpoint_file = "../mongo_atlas_endpoint.env"
  is_files_exist = fileexists(local.env_file) == true && fileexists(local.mongo_atlas_endpoint_file) == true
}

resource "aws_s3_object" "env_file" {

  bucket = aws_s3_bucket.bucket.bucket
  key    = "dev.env"
  # https://discuss.hashicorp.com/t/how-to-upload-a-non-terraform-file-to-terraform-cloud/24894
  # terraform can only upload files&folders in exection directory unless you configured Terraform Working Directory
  # we execute apply command in dev/app folder and dev.env is in dev
  source = local.env_file

  lifecycle {
    precondition {
      condition     = local.is_files_exist
      error_message = "ERROR: missing env file"
    }
  }
}

resource "aws_s3_object" "mongo_atlas_endpoint_file" {

  bucket = aws_s3_bucket.bucket.bucket
  key    = "mongo_atlas_endpoint.env"
  source = local.mongo_atlas_endpoint_file
  lifecycle {
    precondition {
      condition     = local.is_files_exist
      error_message = "ERROR: missing mongo_atlas_endpoint file"
    }
  }
}

# https://discuss.hashicorp.com/t/how-to-create-two-s3-buckets-in-2-different-regions-at-the-same-time-via-terraform/32649
# bucket creation is stick with provider region
# if you want to create bucket in different region, gotta use different aws provider with that region in another module seperately
resource "aws_s3_bucket" "bucket" {
  bucket = "${var.project_name}-env"

  tags = {
    Name = "${var.project_name}-env"
  }
}