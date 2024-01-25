#!/bin/bash
export TF_CLI_CONFIG_FILE="../.terraformrc"

cd infra
terraform destroy -var-file="../general.tfvars" -auto-approve
