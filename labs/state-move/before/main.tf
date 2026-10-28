terraform { required_version = ">= 1.6.0" }
resource "terraform_data" "legacy" { input = "payment-service" }
output "service_name" { value = terraform_data.legacy.output }
