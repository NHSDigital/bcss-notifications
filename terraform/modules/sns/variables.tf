variable "environment" {
  type = string
}

variable "tags" {
  type        = map(string)
  description = "A map of tags to apply to the resource."
}

variable "slack_team_id" {
  type = string
}

variable "slack_channel_id" {
  type = string
}
