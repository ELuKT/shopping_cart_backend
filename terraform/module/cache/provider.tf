terraform {
  required_providers {
    rediscloud = {
      source = "RedisLabs/rediscloud"
      version = "1.3.1"
    }
  }
}

provider "rediscloud" {
  api_key = var.rediscloud_api_key
  secret_key = var.rediscloud_secret_key
}
