variable "pads_auth_token" {
  description = "PaDS auth token for use with the PaDS UserAlerts API"
  type        = string
}

variable "env" {
  description = "Environment name"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "stack_name" {
  description = "Root name for the stack"
}

variable "email_from_address" {
  description = "value for the 'From' field in the email"
  type        = string
}

variable "email_subject_issue_notifications" {
  description = "value for the 'Subject' field in the email"
  type        = string
}

variable "logo_image_url" {
  description = "URL of the logo image to be included in the email"
  type        = string
}

variable "pads_useralerts_url" {
  description = "URL of the PaDS UserAlerts API"
  type        = string
}

variable "web_url" {
  description = "URL of the PEP-Web site"
  type        = string
}
