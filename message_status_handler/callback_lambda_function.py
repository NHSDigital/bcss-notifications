import environment
import json
import logging
import message_status_recorder
import request_verifier
from typing import Dict, Any


def lambda_handler(event: Any, _context: Any) -> Dict[str, Any]:
    logging.info("Message status handler lambda has started. Event: %s", event)
    environment.seed()
    result = {}

    try:
        headers = event.get("headers", {})
        body = event.get("body", "")
        json_body = json.loads(body)

        if request_verifier.verify_request(headers, json_body):
            bcss_response_codes = message_status_recorder.record_message_statuses(json_body)
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
