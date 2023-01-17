terraform {
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

resource "aws_s3_bucket" "pep_subscription_updates" {
  bucket = "pep-subscription-updates-${var.env}"
  tags = {
    STAGE = var.env
  }
}

module "subscription_utility_lambda" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "pep-subscription-mailer-utility-app"
  source_path   = "../app"
  handler       = "subscription_service.handler"
  runtime       = "python3.8"

  environment_variables = {
    "TEST"   = "test-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    "TEEST2" = "test2-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
