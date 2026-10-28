terraform {
  required_version = ">= 1.6.0"
  required_providers {
    random = { source = "hashicorp/random", version = "~> 3.9" }
  }
}
resource "random_id" "existing" {
  byte_length = 4
}
output "imported_id" { value = random_id.existing.b64_url }
