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

variable "slack_webhook_url" {
  description = "Slack webhook URL for sending notifications"
  type        = string
  sensitive   = true
}

variable "slack_notifier_lambda_role_arn" {
  description = "ARN of the IAM role for the Slack notifier Lambda function"
  type        = string
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}
