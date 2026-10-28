terraform { required_version = ">= 1.6.0" }
resource "terraform_data" "service" { input = "payment-service" }
output "service_name" { value = terraform_data.service.output }
