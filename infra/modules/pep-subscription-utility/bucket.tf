resource "aws_s3_bucket" "pep_subscription_updates" {
  bucket = "${var.stack_name}-updates-${var.env}"
  tags = {
    stage = var.env
    stack = var.stack_name
  }
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
