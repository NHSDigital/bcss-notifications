import logging
import hashlib
import time
import uuid
import oracledb
import oracle_database
import random


def next_batch() -> tuple:
    """
    Fetch the next batch ID and routing plan ID.

    Returns:
        tuple: A tuple containing the batch ID and routing plan ID.
    """
    batch_id = generate_batch_id()
    routing_plan_id = get_routing_plan_id(batch_id)
    recipients = None

    if routing_plan_id:
        recipients = get_recipients(batch_id)
    else:
        logging.info("No more remaining batches to process")

    return batch_id, routing_plan_id, recipients


def get_routing_plan_id(batch_id: str) -> str | None:
    return oracle_database.get_routing_plan_id(batch_id)


def get_recipients(batch_id: str) -> list:
    recipients = []
    recipients_results = []

    recipients_results = oracle_database.get_recipients(batch_id)  # []
    if not recipients_results:
        logging.info("No recipients for batch ID: %s", batch_id)

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
    timestamp = time.time_ns()
    rand_bits = random.getrandbits(64)
    str_val = f"{prefix}:{timestamp}:{rand_bits}"
    return str(uuid.UUID(hashlib.md5(str_val.encode()).hexdigest()))
