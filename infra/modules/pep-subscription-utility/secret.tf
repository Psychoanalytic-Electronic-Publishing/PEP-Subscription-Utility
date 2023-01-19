locals {
  pads_auth_token_secret_path = "${var.stack_name}/pads-auth-token/${var.env}"
}

resource "aws_secretsmanager_secret" "pads_auth_token" {
  name        = local.pads_auth_token_secret_path
  description = "PADS auth token for PEP subscription mailer"

  tags = {
    stage = var.env
    stack = var.stack_name
  }
}

resource "aws_secretsmanager_secret_version" "pads_auth_token_version" {
  secret_id     = aws_secretsmanager_secret.pads_auth_token.id
  secret_string = var.pads_auth_token
}
