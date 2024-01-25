# https://developer.hashicorp.com/terraform/language/modules/develop/providers
# https://github.com/hashicorp/terraform/issues/27663
# https://github.com/hashicorp/terraform/issues/25984
# since terraform has some reason not to support 3rd party provider implicit imheritance, nor pass provider explicitly
# we gotta declare its own provider in each module

terraform {
  required_providers {
    mongodbatlas = {
      source = "mongodb/mongodbatlas"
      version = "1.11.0"
    }
  }
}

provider "mongodbatlas" {
  public_key  = var.mongodbatlas_public_key
  private_key = var.mongodbatlas_private_key
}
