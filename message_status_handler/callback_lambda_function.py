import environment
import json
import logging
import message_status_recorder
import request_verifier
from aws_lambda_typing.events import S3Event
from aws_lambda_typing.context import Context

def lambda_handler(event: S3Event, _context: Context) -> dict:
    logging.info("Message status handler lambda has started. Event: %s", event)
    environment.seed()
    result = {}

    try:
        headers = event.get("headers", {})
        body = event.get("body", "")
        json_body = json.loads(body)

        if request_verifier.verify_request(headers, json_body):
            logging.info("Callback request verification successful.")
            bcss_response_codes = message_status_recorder.record_message_statuses(json_body)
            logging.info("Message statuses recorded successfully. Response codes: %s", bcss_response_codes)
            result = {"bcss_response_codes": bcss_response_codes}

        return {
            "status": 200,
            "body": json.dumps(
                {
                    "message": "Message status handler lambda finished",
                    "event": event,
                    "result": result
                }
            ),
        }

    except Exception as e:
        return {
            "status": 500,
            "body": json.dumps({"message": f"Internal Server Error: {e}"}),
        }
