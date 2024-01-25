## prerequisite

terraform cloud
mongodb cloud
redis cloud

### setup redis in redis cloud

### setup a organization in mongodb cloud and create api key

- create api key

    ORGANIZATION -> Access Manager -> Create API Key

- terraform cloud do not have static ip range for whitelist if you are not enterprise tier

    ORGANIZATION -> setttings -> Require IP Access List for the Atlas Administration API -> false

### create general.tfvars with general.tfvars.template

mongodbatlas_org_id: ORGANIZATION -> setttings -> Organization ID
mongodbatlas_public_key: mongodbatlas api public key 
mongodbatlas_private_key: mongodbatlas api private key 

### terraform cloud create organization, Projects, workspaces
- create 3 workspaces: app, infra, nginx

- Workspaces -> Settings -> Terraform Working Directory

    put corresponding value into column in each workspace: dev/app, dev/infra, dev/nginx

### make your terraform cloud able to create aws resources
https://developer.hashicorp.com/terraform/cloud-docs/workspaces/dynamic-provider-credentials/aws-configuration

### make terraform cli able to access terraform cloud
- create team api token
    Settings -> Teams -> Team API Token
    
- create .terraformrc in dev folder with below content
    ```
    credentials "app.terraform.io" {
    token = "team api token"
    }
    ```

### deploy infra

in dev folder, run `./apply-infra.sh`

copy `aws_consul_server_private_ip` from the last output

### create custom nginx image and upload to ecr

in aws-nginx folder

- use nginx.conf.template to create nginx.conf and replace {server_ip} with `aws_consul_server_private_ip`

- run `docker build --no-cache -t aws-nginx:0.1.0 -f Dockerfile .`

- upload nginx image to ecr

### deploy nginx

in dev folder, run `./apply-nginx.sh`

copy `aws_nginx_public_ip` from the last output

copy `aws_nginx_public_dns` from the last output

### create app image and upload to ecr

- run `docker build -t fastapi-sc-backend:0.1.0 -f Dockerfile-aws .` (aws_ecs_task_definition is hardcode version 0.1.0 )

- upload nginx image to ecr

### setup dev.env file(because aws_s3_object is hardcode dev.env as key)

copy .env to dev folder and rename it dev.env

- BASE_URL: http://{aws_nginx_public_dns}/

- REDIS_HOST: use correct value

- REDIS_PORT: use correct value

- REDIS_PASSWORD: change REDIS_PASSWORD with correct value

- DOCS_URL: remove DOCS_URL

### deploy app

in dev folder, run `./apply-app.sh`

### check consul server

http://{aws_nginx_public_dns}/consul-server/

oauth2 login:

http://{aws_nginx_public_dns}/backend/v1/auth/oauth-login


### remove all

run `./destroy.sh`