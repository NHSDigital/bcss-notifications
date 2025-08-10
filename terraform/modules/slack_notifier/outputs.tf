output "slack_notifier_lambda_arn" {
  description = "ARN of the Slack notifier Lambda function"
  value       = aws_lambda_function.slack_notifier.arn
}

output "slack_notifier_lambda_name" {
  description = "Name of the Slack notifier Lambda function"
  value       = aws_lambda_function.slack_notifier.function_name
}

output "lambda_alerts_sns_topic_arn" {
  description = "ARN of the SNS topic for Lambda alerts"
  value       = aws_sns_topic.lambda_alerts.arn
}

output "lambda_alerts_sns_topic_name" {
  description = "Name of the SNS topic for Lambda alerts"
  value       = aws_sns_topic.lambda_alerts.name
}
