data "rediscloud_payment_method" "card" {
  card_type = "Visa"
}

resource "rediscloud_subscription" "subscription" {

  name = "${var.project_name}-subscription"
  memory_storage = "ram"
  payment_method = "credit-card"
  payment_method_id = data.rediscloud_payment_method.card.id

  cloud_provider {
    provider = "AWS"
    region {
      region = var.region
      networking_deployment_cidr = "10.0.0.0/24"
    }
  }

  creation_plan {
    memory_limit_in_gb = 0.03125
    quantity = 1
    throughput_measurement_by = "operations-per-second"
    throughput_measurement_value = 20000
    replication = false # docs says Optional
  }
}