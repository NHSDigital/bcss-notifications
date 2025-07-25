import logging
import hashlib
import time
import uuid
import oracledb
import oracle_database


def next_batch() -> tuple:
    """
    Fetch the next batch ID and routing plan ID.

    Returns:
        tuple: A tuple containing the batch ID and routing plan ID.
    """
    try:
        batch_id = generate_batch_id()
        routing_plan_id = get_routing_plan_id(batch_id)
        recipients = None

        if routing_plan_id:
            recipients = get_recipients(batch_id)

        return batch_id, routing_plan_id, recipients
    except oracledb.Error as e:
        logging.error("Error fetching next batch: %s", e)
        return None, None, None


def get_routing_plan_id(batch_id: str) -> str | None:
    return oracle_database.get_routing_plan_id(batch_id)


def get_recipients(batch_id: str) -> list:
    recipients = []
    recipients_results = []

    try:
        recipients_results = oracle_database.get_recipients(batch_id)
        if not recipients_results:
            logging.error("No recipients for batch ID: %s", batch_id)
    except oracledb.Error as e:
        logging.error("Error fetching recipients: %s", e)

    for recipient in recipients_results:
        recipient = recipient._replace(message_id=generate_message_reference())
        oracle_database.update_message_id(recipient)
        recipients.append(recipient)

    return recipients


def mark_batch_as_sent(batch_id: str) -> None:
    oracle_database.mark_batch_as_sent(batch_id)


def generate_batch_id() -> str:
    return generate_reference("bcss_notify_batch_id")


def generate_message_reference() -> str:
    return generate_reference("bcss_notify_message_reference")


def generate_reference(prefix="") -> str:
    str_val = f"{prefix}:{time.time()}"
    return str(uuid.UUID(hashlib.md5(str_val.encode()).hexdigest()))
