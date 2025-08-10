locals {
  runtime = "python3.13"
}

data "archive_file" "placeholder_zip" {
  type        = "zip"
  output_path = "${path.module}/placeholder.zip"

  source {
    content  = "placeholder"
    filename = "placeholder.txt"
  }
}

# SNS Topic for CloudWatch alarms
resource "aws_sns_topic" "lambda_alerts" {
  name = "${var.team}-${var.project}-lambda-alerts-${var.environment}"
  
  tags = var.tags
}

# SNS Topic subscription to Slack notifier Lambda
resource "aws_sns_topic_subscription" "lambda_alerts_slack" {
  topic_arn = aws_sns_topic.lambda_alerts.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.slack_notifier.arn
}

# Lambda permission for SNS to invoke Slack notifier
resource "aws_lambda_permission" "allow_sns_to_invoke_slack_notifier" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.slack_notifier.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.lambda_alerts.arn
}

# Slack notifier Lambda function
resource "aws_lambda_function" "slack_notifier" {
  filename      = data.archive_file.placeholder_zip.output_path
  function_name = "${var.team}-${var.project}-slack-notifier-${var.environment}"
  handler       = "lambda_function.lambda_handler"
  memory_size   = 128
  role          = var.slack_notifier_lambda_role_arn
  runtime       = local.runtime
  timeout       = 30

  logging_config {
    application_log_level = "INFO"
    log_format           = "JSON"
  }

  environment {
    variables = {
      ENVIRONMENT = var.environment
      SLACK_WEBHOOK_URL = var.slack_webhook_url
    }
  }

  tags = var.tags
}

# CloudWatch Log Group for Slack notifier
resource "aws_cloudwatch_log_group" "slack_notifier" {
  name              = "/aws/lambda/${aws_lambda_function.slack_notifier.function_name}"
  retention_in_days = 14

  tags = var.tags
}
