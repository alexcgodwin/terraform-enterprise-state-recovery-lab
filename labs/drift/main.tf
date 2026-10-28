terraform { required_version = ">= 1.6.0" }
variable "release" {
  type    = string
  default = "v1"
  validation {
    condition     = can(regex("^v[0-9]+$", var.release))
    error_message = "Use v followed by digits."
  }
}
resource "terraform_data" "desired" { input = var.release }
output "deployed_version" { value = terraform_data.desired.output }
