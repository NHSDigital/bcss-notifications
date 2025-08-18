# SNS Topic for error notifications
resource "aws_sns_topic" "error_notifications" {
  name = "bcss-comms-errors-${var.environment}"
  tags = var.tags
}

resource "aws_iam_role" "chatbot" {
  name = "chatbot-slack-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "chatbot.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "chatbot_policy" {
  name = "chatbot-slack-policy"
  role = aws_iam_role.chatbot.id

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "sns:ListSubscriptionsByTopic",
                "sns:ListTopics",
                "sns:Unsubscribe",
                "sns:Subscribe",
                "sns:ListSubscriptions"
            ],
            "Effect": "Allow",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:PutLogEvents",
                "logs:CreateLogStream",
                "logs:DescribeLogStreams",
                "logs:CreateLogGroup",
                "logs:DescribeLogGroups"
            ],
            "Resource": "arn:aws:logs:*:*:log-group:/aws/chatbot/*"
        }
    ]
  })
}

resource "aws_chatbot_slack_channel_configuration" "alerts" {
  configuration_name = "bcss-comms-errors-${var.environment}"
  slack_team_id      = var.slack_team_id
  slack_channel_id   = var.slack_channel_id
  iam_role_arn       = aws_iam_role.chatbot.arn

  # SNS topics in this new account/region that should post to the channel
  sns_topic_arns = [
    aws_sns_topic.error_notifications.arn,
  ]

  logging_level = "ERROR"

  # Guardrail policy to limit to read-only access
  guardrail_policies = [
    "arn:aws:iam::aws:policy/ReadOnlyAccess"
  ]
}