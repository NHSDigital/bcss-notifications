# Lambda Alerting System

This document describes the comprehensive alerting system for AWS Lambda functions in the BCSS Notify Integration project.

## Overview

The alerting system monitors all Lambda functions and sends Slack notifications when they encounter issues or finish with non-success statuses.

## Architecture

```
CloudWatch Alarms → SNS Topic → Slack Notifier Lambda → Slack Channel
```

## Components

### 1. CloudWatch Alarms

The system creates the following alarms for each Lambda function:

- **Errors**: Triggers when any errors occur (threshold: > 0)
- **Duration**: Triggers when execution time exceeds 80% of timeout (threshold: > 4 minutes)
- **Throttles**: Triggers when Lambda is throttled (threshold: > 0)
- **Concurrent Executions**: Triggers when concurrent executions are high (threshold: > 10)

### 2. SNS Topic

- **Name**: `bcss-comms-lambda-alerts-{environment}`
- **Purpose**: Receives CloudWatch alarm notifications and forwards them to the Slack notifier

### 3. Slack Notifier Lambda

- **Function**: `bcss-comms-slack-notifier-{environment}`
- **Purpose**: Processes CloudWatch alarm events and sends formatted messages to Slack
- **Runtime**: Python 3.13
- **Memory**: 128MB
- **Timeout**: 30 seconds

### 4. Slack Integration

- **Method**: Incoming Webhook
- **Format**: Rich message attachments with colour coding
- **Information**: Function name, error details, timestamp, and status

## Configuration

### Environment Variables

The Slack notifier Lambda requires:

```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR_WEBHOOK_URL
ENVIRONMENT=dev|staging|prod
```

### Terraform Variables

```hcl
variable "slack_webhook_url" {
  type        = string
  description = "Slack webhook URL for sending Lambda failure notifications"
  sensitive   = true
}
```

## Monitoring Coverage

The system monitors these Lambda functions:

1. **Batch Notification Processor** (`bcss-comms-batch-notification-processor-{env}`)
2. **Message Status Handler** (`bcss-comms-message-status-handler-{env}`)
3. **Slack Notifier** (`bcss-comms-slack-notifier-{env}`)
4. **Healthcheck** (`bcss-comms-healthcheck-{env}`)
5. **Callback Simulator** (`bcss-comms-callback-simulator-{env}`)

## Alert Triggers

### Immediate Alerts (1 evaluation period)

- **Errors**: Any Lambda function error
- **Throttles**: Lambda function throttling

### Delayed Alerts (2 evaluation periods)

- **Duration**: Lambda execution time approaching timeout
- **Concurrent Executions**: High concurrent execution count

## Slack Message Format

Each alert includes:

- 🚨 **Title**: Clear indication of the issue
- **Status**: Current alarm state (ALARM/OK)
- **Lambda Function**: Name of the affected function
- **Reason**: Why the alarm was triggered
- **Time**: When the issue occurred
- **Colour Coding**: Red for ALARM, Green for OK

## Setup Instructions

### 1. Create Slack Webhook

1. Go to your Slack workspace
2. Navigate to **Apps** → **Incoming Webhooks**
3. Click **Add to Slack**
4. Choose the channel for alerts
5. Copy the webhook URL

### 2. Update Configuration

1. Add the webhook URL to your environment `.tfvars` file:
   ```hcl
   slack_webhook_url = "https://hooks.slack.com/services/YOUR_WEBHOOK_URL"
   ```

2. Deploy the infrastructure:
   ```bash
   terraform plan
   terraform apply
   ```

### 3. Test the System

1. Manually trigger a CloudWatch alarm
2. Verify Slack notification is received
3. Check CloudWatch logs for the Slack notifier

## Troubleshooting

### Common Issues

1. **Slack notifications not received**
   - Check webhook URL is correct
   - Verify Slack notifier Lambda logs
   - Ensure SNS topic subscription is active

2. **Alarms not triggering**
   - Check CloudWatch metrics are being collected
   - Verify alarm thresholds are appropriate
   - Check IAM permissions

3. **High false positive rate**
   - Adjust alarm thresholds
   - Increase evaluation periods for noisy metrics
   - Review Lambda function error handling

### Log Locations

- **Slack Notifier**: `/aws/lambda/bcss-comms-slack-notifier-{env}`
- **CloudWatch Alarms**: Available in CloudWatch console
- **SNS Topic**: Check SNS console for delivery status

## Security Considerations

- Slack webhook URLs are marked as sensitive in Terraform
- IAM roles follow least privilege principle
- CloudWatch logs are retained for 14 days
- All resources are tagged for cost tracking

## Cost Impact

- **CloudWatch Alarms**: ~$0.10 per alarm per month
- **SNS Topic**: ~$0.50 per million notifications
- **Slack Notifier Lambda**: Pay per execution (~$0.0000002 per 100ms)
- **Estimated Total**: < $5/month for typical usage

## Future Enhancements

1. **Escalation Policies**: Route critical alerts to different channels
2. **Alert Suppression**: Prevent alert storms during maintenance
3. **Custom Metrics**: Business-specific monitoring beyond AWS defaults
4. **Dashboard Integration**: CloudWatch dashboards for visual monitoring
5. **PagerDuty Integration**: For critical production alerts
