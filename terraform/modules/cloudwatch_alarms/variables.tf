variable "team" {
  description = "Team name for resource naming"
  type        = string
}

variable "project" {
  description = "Project name for resource naming"
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "lambda_functions" {
  description = "Map of Lambda function names to their function names for monitoring"
  type        = map(string)
  example = {
    "batch-notification-processor" = "bcss-comms-batch-notification-processor-dev"
    "message-status-handler"       = "bcss-comms-message-status-handler-dev"
    "slack-notifier"               = "bcss-comms-slack-notifier-dev"
  }
}

variable "lambda_timeout_threshold_ms" {
  description = "Threshold in milliseconds for Lambda duration alarms (default: 80% of timeout)"
  type        = number
  default     = 240000  # 4 minutes for 5-minute timeout
}

variable "lambda_concurrent_threshold" {
  description = "Threshold for concurrent Lambda executions"
  type        = number
  default     = 10
}

variable "lambda_alerts_sns_topic_arn" {
  description = "ARN of the SNS topic for Lambda alerts"
  type        = string
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
