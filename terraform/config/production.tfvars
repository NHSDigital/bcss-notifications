environment = "prod"
team        = "bcss"
project     = "comms"
region      = "eu-west-2"

# TODO: ARNs TBC
kms_arn       = "arn:aws:kms:eu-west-2:730319765130:key/25da03db-7a99-4a15-bc38-2bf757f27fca"
secrets_arn   = "arn:aws:secretsmanager:eu-west-2:730319765130:secret:TBC"
region        = "eu-west-2"

tags = {
  "Service" = "bcss"
}

# Slack webhook URL for Lambda failure notifications
slack_webhook_url = "https://hooks.slack.com/services/YOUR_PRODUCTION_WEBHOOK_URL_HERE"

