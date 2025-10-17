"""Lambda function to process and send batch notifications via NHS Notify service."""

import batch_processor
import environment
import logging
import notify_api
from aws_lambda_typing.events import S3Event
from aws_lambda_typing.context import Context


def lambda_handler(_event: S3Event, _context: Context) -> dict:
    """
    AWS Lambda handler to process and send batch notifications.
    """
    logging.info("Batch notification processor lambda function has started.")

    environment.seed()

    batch_id, routing_plan_id, recipients = batch_processor.next_batch()
    batches = []

    while routing_plan_id and recipients:

        logging.info(
            "Processing next batch. (batch_id: %s, routing_plan_id: %s, recipients_count: %d)",
            batch_id,
            routing_plan_id,
            len(recipients),
        )

        response = notify_api.send_batch_message(batch_id, routing_plan_id, recipients)

        if response.status_code == 201:

            result = batch_processor.mark_batch_as_sent(batch_id)

            if result is not None and result > 0:
                logging.error(
                    "Failed to mark batch %s as sent. Result code: %s", batch_id, result
                )

            batches.append(batch_id)
            logging.info(
                "Batch %s sent successfully to %s recipients.",
                batch_id,
                len(recipients),
            )
        else:
            logging.error(
                "Batch %s failed to send. Status code: %s. Response: %s",
                batch_id,
                response.status_code,
                response.text,
            )

        batch_id, routing_plan_id, recipients = batch_processor.next_batch()

    logging.info(
        "Batch notification processor lambda function has completed processing. Total batches sent: %d",
        len(batches),
    )

    return {
        "status": "complete",
        "message": f"Processed batches: {len(batches)}",
    }
