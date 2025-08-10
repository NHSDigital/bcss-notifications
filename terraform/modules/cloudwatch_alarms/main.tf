# CloudWatch Alarm for Lambda function errors
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  for_each = var.lambda_functions

  alarm_name          = "${var.team}-${var.project}-${each.key}-errors-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Lambda function ${each.key} has encountered errors"
  alarm_actions       = [var.lambda_alerts_sns_topic_arn]
  ok_actions          = [var.lambda_alerts_sns_topic_arn]

  dimensions = {
    FunctionName = each.value
  }

  tags = var.tags
}

# CloudWatch Alarm for Lambda function duration (timeout risk)
resource "aws_cloudwatch_metric_alarm" "lambda_duration" {
  for_each = var.lambda_functions

  alarm_name          = "${var.team}-${var.project}-${each.key}-duration-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "Duration"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Average"
  threshold           = var.lambda_timeout_threshold_ms
  alarm_description   = "Lambda function ${each.key} is taking longer than expected to execute"
  alarm_actions       = [var.lambda_alerts_sns_topic_arn]
  ok_actions          = [var.lambda_alerts_sns_topic_arn]

  dimensions = {
    FunctionName = each.value
  }

  tags = var.tags
}

# CloudWatch Alarm for Lambda function throttles
resource "aws_cloudwatch_metric_alarm" "lambda_throttles" {
  for_each = var.lambda_functions

  alarm_name          = "${var.team}-${var.project}-${each.key}-throttles-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Lambda function ${each.key} is being throttled"
  alarm_actions       = [var.lambda_alerts_sns_topic_arn]
  ok_actions          = [var.lambda_alerts_sns_topic_arn]

  dimensions = {
    FunctionName = each.value
  }

  tags = var.tags
}

# CloudWatch Alarm for Lambda function concurrent executions
resource "aws_cloudwatch_metric_alarm" "lambda_concurrent_executions" {
  for_each = var.lambda_functions

  alarm_name          = "${var.team}-${var.project}-${each.key}-concurrent-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "ConcurrentExecutions"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Maximum"
  threshold           = var.lambda_concurrent_threshold
  alarm_description   = "Lambda function ${each.key} has high concurrent execution count"
  alarm_actions       = [var.lambda_alerts_sns_topic_arn]
  ok_actions          = [var.lambda_alerts_sns_topic_arn]

  dimensions = {
    FunctionName = each.value
  }

  tags = var.tags
}
