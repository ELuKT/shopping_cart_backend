#!/bin/bash
# we run apply in app, infra and nginx folder
export TF_CLI_CONFIG_FILE="../.terraformrc"

cd infra

terraform init
terraform apply -var-file="../general.tfvars" -auto-approve

if [ $? -ne 0 ];then
 exit 1
fi

MONGODB_URL="$(terraform output mongo_atlas_endpoint | sed 's/"//g')" # remove double quote cus ecs can not tolerant quote like local docker does
username=$(cat ../general.tfvars | grep mongodbatlas_database_username | awk -F= '{print $2}' | sed 's/"//g')
password=$(cat ../general.tfvars | grep mongodbatlas_database_password | awk -F= '{print $2}' | sed 's/"//g')
p=10 # char of mongodb://
MONGODB_URL="${MONGODB_URL:0:p}$username:$password@${MONGODB_URL:p}"
echo "MONGODB_URL=$MONGODB_URL" > ../mongo_atlas_endpoint.env
