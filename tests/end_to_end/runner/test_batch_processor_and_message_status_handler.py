import json
import logging
import os
import pytest
import requests
import time
import uuid

from request_verifier import create_digest


def test_batch_processor_and_message_status_handler_lambdas(helpers, recipient_data):
    """
    Test that the batch processor lambda sends to NHS Notify /v1/message-batches endpoint.
    Assert that successfully sent messages are marked as 'sending' in the message queue.
    Simulate callbacks from NHS Notify which are then received by the message status handler lambda.
    Assert that the message status handler lambda processes the callbacks and marks messages as 'read' in the message queue.
    """
    helpers.seed_message_queue(recipient_data)
    trigger_batch_notification_processor_lambda() # IRL this is a scheduled lambda function call at 0800hrs and 0900hrs.

    with helpers.cursor() as cursor:
        send_all_status_callbacks(cursor, recipient_data)

        cursor.execute(
            (
                "SELECT nhs_number "
                "FROM v_notify_message_queue "
                "WHERE message_status = 'read' "
            )
        )
        results = cursor.fetchall()
        assert len(results) == len(recipient_data), "Not all messages were marked as read"
        for result in results:
            assert result[0] in recipient_data, "NHS number not found in recipient data"


def trigger_batch_notification_processor_lambda():
    response = requests.post("http://localhost:9000/2015-03-31/functions/function/invocations", json={})
    logging.debug("Response: %s", response.json())


def send_all_status_callbacks(cursor, recipient_data):
    cursor.execute(
        (
            "SELECT message_id "
            "FROM v_notify_message_queue "
            "WHERE message_status = 'sending'"
            "AND nhs_number IN {}".format(tuple(recipient_data))
        )
    )
    results = cursor.fetchall()
    assert len(results) == len(recipient_data), "Not all messages were marked as sending"

    for r in results:
        send_status_callbacks({"id": uid(27), "messageReference": r[0]})


def send_status_callbacks(message):
    post_callback(channel_status(message, status="sending", supplier_status="received"))
    post_callback(channel_status(message, supplier_status="notified"))
    post_callback(channel_status(message, supplier_status="read"))
    post_callback(message_status(message))


def post_callback(post_body):
    client_endpoint = "http://localhost:9001/2015-03-31/functions/function/invocations"
    signature_secret = f"{os.getenv('APPLICATION_ID')}.{os.getenv('API_KEY')}"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.getenv("API_KEY"),
        "x-hmac-sha256-signature": create_digest(signature_secret, json.dumps(post_body, sort_keys=True))
    }
    # Emulate an AWS Lambda function URL payload structure
    # See https://docs.aws.amazon.com/lambda/latest/dg/urls-invocation.html#urls-payloads
    aws_lambda_post_body = {
        "version": "2.0",
        "routeKey": "POST /status/update",
        "rawPath": "/status/update",
        "rawQueryString": "",
        "cookies": [],
        "headers": headers,
        "body": json.dumps(post_body, sort_keys=True),
        "requestContext": {},
        "isBase64Encoded": False
    }
    response = requests.post(client_endpoint, headers=headers, json=aws_lambda_post_body)
    logging.debug("Response from callback: %s: %s", response.status_code, response.text)

    if response.status_code != 200:
        pytest.fail(f"Failed to post callback: {response.status_code} - {response.text}")


def channel_status(message, status="delivered", supplier_status="read"):
    return {
        "data": [
            {
                "type": "ChannelStatus",
                "attributes": {
                    "messageId": message["id"],
                    "messageReference": message["messageReference"],
                    "cascadeType": "primary",
                    "cascadeOrder": 1,
                    "channel": "nhsapp",
                    "channelStatus": status,
                    "channelStatusDescription": " ",
                    "supplierStatus": supplier_status,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "retryCount": 1
                },
                "links": {
                    "message": f"http://nhs-notify-api-stub/comms/v1/messages/{message['id']}"
                },
                "meta": {
                    "idempotencyKey": uid(64) #gitleaks:allow
                }
            }
        ]
    }


def message_status(message, message_status="sending", channel_status="delivered"):
    return {
        "data": [
            {
                "type": "MessageStatus",
                "attributes": {
                    "messageId": message["id"],
                    "messageReference": message["messageReference"],
                    "messageStatus": message_status,
                    "messageStatusDescription": " ",
                    "channels": [
                        {
                            "type": "email",
                            "channelStatus": channel_status
                        }
                    ],
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "routingPlan": {
                        "id": "b838b13c-f98c-4def-93f0-515d4e4f4ee1",
                        "name": "Plan Abc",
                        "version": "ztoe2qRAM8M8vS0bqajhyEBcvXacrGPp",
                        "createdDate": "2023-11-17T14:27:51.413Z"
                    }
                },
                "links": {
                    "message": f"http://nhs-notify-api-stub/comms/v1/messages/{message['id']}"
                },
                "meta": {
                    "idempotencyKey": uid(64) #gitleaks:allow
                }
            }
        ]
    }


def uid(length):
    return uuid.uuid4().hex[:length]
