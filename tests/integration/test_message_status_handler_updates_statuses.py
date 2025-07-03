import dotenv
import json
import uuid

from request_verifier import create_digest, notify_api_key, signature_secret

dotenv.load_dotenv(".env.test")

import callback_lambda_function as lambda_function


def test_message_status_handler_updates_message_status(recipient_data, helpers):
    """Test that the message status handler updates the message statuses correctly."""
    batch_id = str(uuid.uuid4())
    message_references = [r[1] for r in recipient_data]
    helpers.seed_message_queue(batch_id, recipient_data)
    helpers.call_get_next_batch(batch_id)
    helpers.mark_batch_as_sent(batch_id)
    request_body = {
        "data": [
            {
                "type": "ChannelStatus",
                "attributes": {
                    "channel": "nhsapp",
                    "supplierStatus": "read",
                    "messageReference": message_references[0]
                }
            }
        ]
    }
    body_str = json.dumps(request_body)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-hmac-sha256-signature": create_digest(signature_secret(), body_str),
        "x-api-key": notify_api_key(),
    }

    lambda_function.lambda_handler({
        "headers": headers,
        "body": body_str
    }, {})

    with helpers.cursor() as cur:
        cur.execute(
            "SELECT message_id FROM v_notify_message_queue WHERE batch_id = :batch_id AND message_status = 'read'",
            batch_id=batch_id
        )
        results = cur.fetchall()

    assert len(results) == 1
    assert results[0][0] == message_references[0]


def test_message_status_handler_invalid_request(helpers):
    """Test that the message status handler does nothing for invalid requests."""
    request_body = {
        "data": [
            {
                "type": "ChannelStatus",
                "attributes": {
                    "channel": "nhsapp",
                    "supplierStatus": "read",
                    "messageId": "invalid-message-id"
                }
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-hmac-sha256-signature": create_digest(signature_secret(), json.dumps(request_body, sort_keys=True)),
        "x-api-key": notify_api_key(),
    }

    lambda_function.lambda_handler({
        "headers": headers,
        "body": json.dumps(request_body)
    }, {})

    with helpers.cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) FROM v_notify_message_queue WHERE message_status = 'read'"
        )
        count = cur.fetchone()[0]

    assert count == 0
