resource "mongodbatlas_project" "project" {
  name   = "${var.project_name}-project"
  org_id = "${var.mongodbatlas_org_id}"

  limits {
    name = "atlas.project.deployment.clusters"
    value = 1
  }

  is_collect_database_specifics_statistics_enabled = true
  is_realtime_performance_panel_enabled            = true
  is_schema_advisor_enabled                        = true
}

# https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/#operational-limitations
# you cannot modify an M0 free cluster using the Clusters API resource.(but can create)
# use terraform destroy a single resource and create again

# The primary difference between mongodbatlas_cluster and mongodbatlas_advanced_cluster is that mongodbatlas_advanced_cluster supports multi-cloud clusters

resource "mongodbatlas_advanced_cluster" "advanced_cluster" {
  project_id   = mongodbatlas_project.project.id
  name         = "${var.project_name}-ac"
  cluster_type = "REPLICASET"
  replication_specs {
    region_configs {
      electable_specs {
        # https://www.mongodb.com/docs/atlas/reference/amazon-aws/#amazon-web-services--aws-
        instance_size = "M0"
      }
      # https://www.mongodb.com/docs/atlas/reference/amazon-aws/#amazon-web-services--aws-
      region_name     = "AP_NORTHEAST_1"
      # https://www.mongodb.com/community/forums/t/is-it-possible-to-create-a-standalone-db-single-node-in-mongo-atlas/109886
      priority        = 7
      provider_name = "TENANT"
      backing_provider_name = "AWS"
    }
    
  }
}


resource "mongodbatlas_project_ip_access_list" "ip_access_list" {
  project_id = mongodbatlas_project.project.id
  ip_address = "${var.aws_nat_gateway_ip}"
  comment    = "aws nat gateway ip"
}

resource "mongodbatlas_database_user" "user" {
  username           = "${var.mongodbatlas_database_username}"
  password           = "${var.mongodbatlas_database_password}"
  project_id         = mongodbatlas_project.project.id
  auth_database_name = "admin" # Accepted values include: admin, $external

  roles {
    role_name     = "readWrite"
    database_name = "${var.mongodbatlas_database_name}"
  }
}
