terraform {
  backend "s3" {
    key = "global/s3/subscription-updates-stage.tfstate"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = var.aws_region
}


module "pep_subscription_utility" {
  source = "../modules/pep-subscription-utility"

  env                               = var.env
  aws_region                        = var.aws_region
  stack_name                        = var.stack_name
  email_from_address                = var.email_from_address
  email_subject_issue_notifications = var.email_subject_issue_notifications
  logo_image_url                    = var.logo_image_url
  pads_useralerts_url               = var.pads_useralerts_url
  web_url                           = var.web_url
  pads_auth_token                   = var.pads_auth_token
}
