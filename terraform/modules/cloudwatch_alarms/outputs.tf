output "lambda_error_alarms" {
  description = "Map of Lambda error alarm names to their ARNs"
  value       = {
    for k, v in aws_cloudwatch_metric_alarm.lambda_errors : k => v.arn
  }
}

output "lambda_duration_alarms" {
  description = "Map of Lambda duration alarm names to their ARNs"
  value       = {
    for k, v in aws_cloudwatch_metric_alarm.lambda_duration : k => v.arn
  }
}

output "lambda_throttle_alarms" {
  description = "Map of Lambda throttle alarm names to their ARNs"
  value       = {
    for k, v in aws_cloudwatch_metric_alarm.lambda_throttles : k => v.arn
  }
}

output "lambda_concurrent_alarms" {
  description = "Map of Lambda concurrent execution alarm names to their ARNs"
  value       = {
    for k, v in aws_cloudwatch_metric_alarm.lambda_concurrent_executions : k => v.arn
  }
}

output "all_alarm_arns" {
  description = "List of all CloudWatch alarm ARNs"
  value       = concat(
    [for alarm in aws_cloudwatch_metric_alarm.lambda_errors : alarm.arn],
    [for alarm in aws_cloudwatch_metric_alarm.lambda_duration : alarm.arn],
    [for alarm in aws_cloudwatch_metric_alarm.lambda_throttles : alarm.arn],
    [for alarm in aws_cloudwatch_metric_alarm.lambda_concurrent_executions : alarm.arn]
  )
}
