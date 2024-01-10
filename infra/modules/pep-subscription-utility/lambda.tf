module "subscription_utility_lambda" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${var.stack_name}-handler-${var.env}"
  source_path   = "../../app"
  handler       = "subscription_service.handler"
  runtime       = "python3.8"
  timeout       = 900

  tags = {
    stage = var.env
    stack = var.stack_name
  }

  environment_variables = {
    "PADS_AUTH_TOKEN_SECRET"            = local.pads_auth_token_secret_path
    "EMAIL_FROM_ADDRESS"                = var.email_from_address
    "EMAIL_SUBJECT_ISSUE_NOTIFICATIONS" = var.email_subject_issue_notifications
    "LOGO_IMAGE_URL"                    = var.logo_image_url
    "PADS_USERALERTS_URL"               = var.pads_useralerts_url
    "S3_BUCKET_SUBSCRIPTIONS"           = aws_s3_bucket.pep_subscription_updates.id
    "WEB_URL"                           = var.web_url
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


resource "aws_iam_role_policy" "ses_policy" {
  name = "ses_access_permissions"
  role = module.subscription_utility_lambda.lambda_role_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role_policy" "s3_policy" {
  name = "s3_access_permissions"
  role = module.subscription_utility_lambda.lambda_role_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:HeadObject"
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.pep_subscription_updates.arn}/*"
      },
    ]
  })
}
