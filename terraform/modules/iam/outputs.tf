output "batch_notification_processor_lambda_role_arn" {
  value = aws_iam_role.batch_notification_processor_lambda_role.arn
}

output "message_status_handler_lambda_role_arn" {
  value = aws_iam_role.message_status_handler_lambda_role.arn
}

output "healthcheck_lambda_role_arn" {
  value = aws_iam_role.healthcheck_lambda_role.arn
}

output "callback_simulator_lambda_role_arn" {
  value = aws_iam_role.callback_simulator_lambda_role.arn
}

output "slack_notifier_lambda_role_arn" {
  value = aws_iam_role.slack_notifier_lambda_role.arn
}
