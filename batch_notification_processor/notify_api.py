import access_token
import hashlib
import hmac
import json
import logging
import os
import uuid
from recipient import Recipient
import requests


def send_batch_message(
    batch_id: str,
    routing_config_id: str,
    recipients: list[Recipient],
) -> requests.Response:
    request_body: dict = generate_batch_message_request_body(
        routing_config_id, batch_id, recipients
    )

    headers = {
        "content-type": "application/vnd.api+json",
        "accept": "application/vnd.api+json",
        "x-correlation-id": str(uuid.uuid4()),
        "authorization": f"Bearer {access_token.get_token()}"
    }

    url = f"{os.getenv('NOTIFY_API_BASE_URL')}/v1/message-batches"

    response = requests.post(
        url,
        headers=headers,
        json=request_body,
        timeout=10
    )

    return response

def generate_batch_message_request_body(
    routing_config_id: str, message_batch_reference: str, recipients: list[Recipient]
) -> dict:
    return {
        "data": {
            "type": "MessageBatch",
            "attributes": {
                "routingPlanId": routing_config_id,
                "messageBatchReference": message_batch_reference,
                "messages": [generate_message(r) for r in recipients],
            },
        }
    }


# pylint: disable=no-member
def generate_message(recipient) -> dict:
    return {
        "messageReference": recipient.message_id,
        "recipient": {"nhsNumber": recipient.nhs_number},
        "personalisation": {
            "address_line_1_bcss": recipient.address_line_1,
            "address_line_2_bcss": recipient.address_line_2,
            "address_line_3_bcss": recipient.address_line_3,
            "address_line_4_bcss": recipient.address_line_4,
            "address_line_5_bcss": recipient.address_line_5,
            "address_line_6_bcss": recipient.postcode,
        },
    }
# pylint: enable=no-member