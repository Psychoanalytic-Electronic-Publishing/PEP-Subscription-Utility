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

locals {
  pads_auth_token_secret_path = "${var.stack_name}/pads-auth-token/${var.env}"
}

resource "aws_secretsmanager_secret" "pads_auth_token" {
  name        = local.pads_auth_token_secret_path
  description = "Pads auth token for pep subscription mailer"

  tags = {
    stage = var.env
    stack = var.stack_name
  }
}

resource "aws_secretsmanager_secret_version" "pads_auth_token_version" {
  secret_id     = aws_secretsmanager_secret.pads_auth_token.id
  secret_string = var.pads_auth_token
}

resource "aws_s3_bucket" "pep_subscription_updates" {
  bucket = "${var.stack_name}-updates-${var.env}"
  tags = {
    stage = var.env
    stack = var.stack_name
  }
}

module "subscription_utility_lambda" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${var.stack_name}-handler-${var.env}"
  source_path   = "../app"
  handler       = "subscription_service.handler"
  runtime       = "python3.8"

  tags = {
    stage = var.env
    stack = var.stack_name
  }

  environment_variables = {
    "PADS_AUTH_TOKEN_SECRET" = local.pads_auth_token_secret_path
  }
}

resource "aws_iam_role_policy" "sm_policy" {
  name = "sm_access_permissions"
  role = module.subscription_utility_lambda.lambda_role_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "secretsmanager:GetSecretValue",
        ]
        Effect   = "Allow"
        Resource = aws_secretsmanager_secret.pads_auth_token.arn
      },
    ]
  })
}


resource "aws_s3_bucket_notification" "pep_subscription_notification" {
  bucket = aws_s3_bucket.pep_subscription_updates.id

  lambda_function {
    lambda_function_arn = module.subscription_utility_lambda.lambda_function_arn
    events              = ["s3:ObjectCreated:*"]
  }
}


resource "aws_lambda_permission" "allow_bucket_invoke" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = module.subscription_utility_lambda.lambda_function_arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.pep_subscription_updates.arn
}
