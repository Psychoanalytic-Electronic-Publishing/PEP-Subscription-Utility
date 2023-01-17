# Environment variables
variable "pads_auth_token" {
  type = string
}

# Local variables
variable "env" {
  default = "dev"
}

variable "aws_region" {
  default = "us-east-1"
}

variable "stack_name" {
  default = "pep-subscription-mailer"
}
