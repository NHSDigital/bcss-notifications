"""Lambda function to send Slack notifications for failed Lambda executions."""

import json
import logging
import os
import urllib.request
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def lambda_handler(event: Dict[str, Any], _context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler to send Slack notifications for failed Lambda executions.
    
    Expected event format from CloudWatch Alarm:
    {
        "AlarmName": "Lambda Function Failed",
        "AlarmDescription": "Lambda function finished with non-success status",
        "NewStateValue": "ALARM",
        "NewStateReason": "Threshold Crossed",
        "StateChangeTime": "2024-01-01T00:00:00.000Z",
        "Trigger": {
            "MetricName": "Duration",
            "Namespace": "AWS/Lambda",
            "Statistic": "Average",
            "Unit": "Milliseconds"
        }
    }
    """
    logger.info("Slack notifier lambda has started. Event: %s", event)
    
    try:
        # Extract Slack webhook URL from environment
        slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
        if not slack_webhook_url:
            logger.error("SLACK_WEBHOOK_URL environment variable not set")
            return {"statusCode": 500, "body": "Slack webhook URL not configured"}
        
        # Parse the CloudWatch alarm event
        alarm_name = event.get('AlarmName', 'Unknown Alarm')
        alarm_description = event.get('AlarmDescription', 'No description available')
        new_state = event.get('NewStateValue', 'Unknown')
        state_reason = event.get('NewStateReason', 'No reason provided')
        state_change_time = event.get('StateChangeTime', 'Unknown time')
        
        # Create Slack message
        slack_message = create_slack_message(
            alarm_name, alarm_description, new_state, 
            state_reason, state_change_time, event
        )
        
        # Send to Slack
        send_slack_notification(slack_webhook_url, slack_message)
        
        logger.info("Slack notification sent successfully")
        return {"statusCode": 200, "body": "Slack notification sent"}
        
    except Exception as e:
        logger.error("Failed to send Slack notification: %s", str(e))
        return {"statusCode": 500, "body": f"Failed to send notification: {str(e)}"}


def create_slack_message(alarm_name: str, alarm_description: str, new_state: str, 
                        state_reason: str, state_change_time: str, 
                        event: Dict[str, Any]) -> Dict[str, Any]:
    """Create a formatted Slack message for the CloudWatch alarm."""
    
    # Determine colour based on alarm state
    colour = "#ff0000" if new_state == "ALARM" else "#36a64f"
    
    # Extract Lambda function name if available
    lambda_function_name = "Unknown"
    if 'Trigger' in event and 'Dimensions' in event['Trigger']:
        for dimension in event['Trigger']['Dimensions']:
            if dimension.get('Name') == 'FunctionName':
                lambda_function_name = dimension.get('Value', 'Unknown')
                break
    
    # Create Slack message with British English
    message = {
        "attachments": [
            {
                "colour": colour,
                "title": f"🚨 AWS Lambda Alert: {alarm_name}",
                "text": alarm_description,
                "fields": [
                    {
                        "title": "Status",
                        "value": new_state,
                        "short": True
                    },
                    {
                        "title": "Lambda Function",
                        "value": lambda_function_name,
                        "short": True
                    },
                    {
                        "title": "Reason",
                        "value": state_reason,
                        "short": True
                    },
                    {
                        "title": "Time",
                        "value": state_change_time,
                        "short": True
                    }
                ],
                "footer": "BCSS Notify Integration",
                "ts": int(state_change_time.replace("Z", "").replace(":", "").replace("-", "").replace(".", ""))
            }
        ]
    }
    
    return message


def send_slack_notification(webhook_url: str, message: Dict[str, Any]) -> None:
    """Send the Slack notification via webhook."""
    
    # Convert message to JSON
    json_data = json.dumps(message).encode('utf-8')
    
    # Create HTTP request
    req = urllib.request.Request(
        webhook_url,
        data=json_data,
        headers={'Content-Type': 'application/json'}
    )
    
    # Send request
    with urllib.request.urlopen(req) as response:
        if response.status != 200:
            raise Exception(f"Slack webhook returned status {response.status}")
        
        logger.info("Slack webhook response: %s", response.read().decode('utf-8'))
