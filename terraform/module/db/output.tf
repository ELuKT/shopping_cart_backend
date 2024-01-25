output "mongodb_endpoint" {
  value = mongodbatlas_advanced_cluster.advanced_cluster.connection_strings[0].standard
}
