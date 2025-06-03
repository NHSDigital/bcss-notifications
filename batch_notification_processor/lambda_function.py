"""Lambda function to process and send batch notifications via NHS Notify service."""

import batch_processor
import environment
import logging
import communication_management

def lambda_handler(_event: dict, _context: object) -> dict:
    """
    AWS Lambda handler to process and send batch notifications.
    """
    logging.info("Batch notification processor lambda function has started.")

    environment.seed()

    batch_id, routing_plan_id, recipients = batch_processor.next_batch()
    batches = []

    logging.info("Processing next batch. (batch_id: %s, routing_plan_id: %s, recipients: %s)", batch_id, routing_plan_id, recipients)

    while routing_plan_id and recipients:
        response = communication_management.send_batch_message(
            batch_id, routing_plan_id, recipients
        )

        if response.status_code == 201:
            batch_processor.mark_batch_as_sent(batch_id)
            batches.append({"batch_id": batch_id, "routing_plan_id": routing_plan_id, "recipients": recipients})
            logging.info("Batch %s sent successfully to %s recipients.", batch_id, len(recipients))
        else:
            logging.error("Batch %s failed to send. Status code: %s. Response: %s", batch_id, response.status_code, response.text)

        batch_id, routing_plan_id, recipients = batch_processor.next_batch()

    logging.info("Batch notification processor lambda function has completed processing. Batches sent: %s", batches)

    return {
        "status": "complete",
        "message": f"Processed batches: {batches}",
    }
