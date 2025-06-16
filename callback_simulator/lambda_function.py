import hashlib
import hmac
import json
import logging
import os
import time
import uuid
import requests
import database
import environment


def lambda_handler(_event, _context):
    environment.seed()

    logging.info("Sending message status callbacks")
    responses = send_status_callbacks()
    logging.info("Sent %d message status callbacks", len(responses))

    return {
        "status": 200,
        "body": json.dumps({
            "message": "Message status callbacks sent successfully",
            "responses": responses
        })
    }


def send_status_callbacks():
    with database.cursor() as cursor:
        cursor.execute(
            (
                "SELECT message_id "
                "FROM v_notify_message_queue "
                "WHERE message_status = 'sending'"
            )
        )

        results = cursor.fetchall()

    responses = []

    for r in results:
        response = post_callback(channel_status({"id": uid(27), "messageReference": r[0]}))
        if response.status_code != 200:
            logging.error("Failed to post callback for message %s: %s", r[0], response.text)

        responses.append(response.json())

    return responses


def post_callback(post_body):
    endpoint = os.getenv('MESSAGE_STATUS_HANDLER_LAMBDA_URL')
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.getenv("OAUTH_API_KEY"),
        "x-hmac-sha256-signature": create_digest(json.dumps(post_body, sort_keys=True))
    }
    response = requests.post(endpoint, headers=headers, json=post_body)
    logging.debug("Response from callback: %s: %s", response.status_code, response.text)

    if not response or response.status_code != 200:
        raise Exception(f"Failed to post callback: {response.status_code} - {response.text}")

    return response


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
                    "message": f"https://int.api.service.nhs.uk/comms/v1/messages/{message['id']}"
                },
                "meta": {
                    "idempotencyKey": uid(64)  # gitleaks:allow
                }
            }
        ]
    }


def uid(length):
    return uuid.uuid4().hex[:length]

# pylint: disable=duplicate-code
def create_digest(message: str) -> str:
    secret = f"{os.getenv('APPLICATION_ID')}.{os.getenv('OAUTH_API_KEY')}"
    return hmac.new(
        bytes(secret, 'ASCII'),
        msg=bytes(message, 'ASCII'),
        digestmod=hashlib.sha256
    ).hexdigest()
