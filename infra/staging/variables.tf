# Environment variables
variable "pads_auth_token" {
  description = "Pads auth token for use with the PADS UserAlerts API"
  type        = string
}

# Local variables
variable "env" {
  description = "Environment name"
  default     = "staging"
}

variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "stack_name" {
  description = "Root name for the stack"
  default     = "pep-subscription-updates"
}

variable "email_from_address" {
  description = "value for the 'From' field in the email"
  type        = string
  default     = "no-reply@pep-web.org"
}

variable "email_subject_issue_notifications" {
  description = "value for the 'Subject' field in the email"
  type        = string
  default     = "PEP Stage Update Alert"
}

variable "logo_image_url" {
  description = "URL of the logo image to be included in the email"
  type        = string
  default     = "https://stage-api.pep-web.org/v2/Documents/Image"
}

variable "pads_useralerts_url" {
  description = "URL of the PADS UserAlerts API"
  type        = string
  default     = "https://stage-pads.pep-web.org/pepsecure/api/v1/UserAlerts"
}

variable "web_url" {
  description = "URL of the PEP-Web site"
  type        = string
  default     = "https://stage.pep-web.org"
}

fwaifnwaifgn 
