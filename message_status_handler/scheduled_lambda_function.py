import communication_management
import environment
import json
import logging
import batch_fetcher
import message_status_recorder
from typing import Dict, Any


def lambda_handler(_event: Any, _context: Any) -> Dict[str, Any]:
    logging.info("Message status handler lambda has started.")
    environment.seed()
    results = {}
    try:
        batch_ids = batch_fetcher.fetch_batch_ids()
        for batch_id in batch_ids:
            results[batch_id] = {}
            messages_with_read_status = communication_management.get_read_messages(batch_id)
            logging.info(
                "Processing %s messages with read status for batch_id: %s", 
                len(messages_with_read_status),
                batch_id
            )
            results[batch_id]["notification_status"] = messages_with_read_status

            if len(messages_with_read_status) > 0:
                bcss_responses = message_status_recorder.record_message_statuses(batch_id, messages_with_read_status)
                results[batch_id]["bcss_response"] = bcss_responses

        logging.info("Message status handler lambda has finished.")
        logging.info("Results: %s", results)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Message status handler lambda finished",
                    "data": results,
                }
            ),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Internal Server Error: {e}"}),
        }
