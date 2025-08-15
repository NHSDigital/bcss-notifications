# Schedule to trigger the Batch Notification Processor Lambda at 8:00 every day
resource "aws_cloudwatch_event_rule" "batch_notification_processor_8am_schedule" {
  name                = "batch-notification-processor-8am-schedule-${var.environment}"
  description         = "Schedule for batch notification processor lambda at 08:00"
  schedule_expression = "cron(0 8 * * ? *)"
  state               = "DISABLED"
}

# Schedule to trigger the Batch Notification Processor Lambda at 9:00 every day
resource "aws_cloudwatch_event_rule" "batch_notification_processor_9am_schedule" {
  name                = "batch-notification-processor-9am-schedule-${var.environment}"
  description         = "Schedule for batch notification processor lambda at 09:00"
  schedule_expression = "cron(0 9 * * ? *)"
  state               = "DISABLED"
}

resource "aws_cloudwatch_event_target" "batch_notification_processor_8am_event_target" {
  rule      = aws_cloudwatch_event_rule.batch_notification_processor_8am_schedule.name
  target_id = "batch_notification_processor_8am_event_target"
  arn       = var.batch_notification_processor_lambda_arn
}

resource "aws_cloudwatch_event_target" "batch_notification_processor_9am_event_target" {
  rule      = aws_cloudwatch_event_rule.batch_notification_processor_9am_schedule.name
  target_id = "batch_notification_processor_9am_event_target"
  arn       = var.batch_notification_processor_lambda_arn
}

# Grant CloudWatch Events permission to invoke the Batch Notification Processor Lambda function
resource "aws_lambda_permission" "allow_cloudwatch_8am_to_call_batch_notification_processor" {
  statement_id  = "AllowExecutionFromCloudWatch-8am"
  action        = "lambda:InvokeFunction"
  function_name = var.batch_notification_processor_lambda_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.batch_notification_processor_8am_schedule.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_9am_to_call_batch_notification_processor" {
  statement_id  = "AllowExecutionFromCloudWatch-9am"
  action        = "lambda:InvokeFunction"
  function_name = var.batch_notification_processor_lambda_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.batch_notification_processor_9am_schedule.arn
}
