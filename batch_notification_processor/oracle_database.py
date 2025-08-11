import logging
import oracledb
import database

from recipient import Recipient


def get_routing_plan_id(batch_id: str) -> str | None:
    with database.cursor() as cursor:
        try:
            result = cursor.callfunc(
                "PKG_NOTIFY_WRAP.f_get_next_batch", oracledb.STRING, [batch_id]
            )
            cursor.connection.commit()
            return result
        except oracledb.Error as e:
            logging.error(
                "Error calling PKG_NOTIFY_WRAP.f_get_next_batch for batch_id %s: %s",
                batch_id,
                e,
            )
            return None


def get_recipients(batch_id: str) -> list[Recipient]:
    recipient_data = []

    with database.cursor() as cursor:
        try:
            cursor.execute(
                """
                SELECT nhs_number,
                       message_id,
                       address_line_1,
                       address_line_2,
                       address_line_3,
                       address_line_4,
                       address_line_5,
                       postcode
                FROM v_notify_message_queue
                WHERE batch_id = :batch_id
                """,
                {"batch_id": batch_id},
            )
            recipient_data = cursor.fetchall()
        except oracledb.Error as e:
            logging.error("Error retrieving recipients for batch: %s", e)

    return [Recipient(*rd) for rd in recipient_data]


def mark_batch_as_sent(batch_id: str) -> int | None:
    with database.cursor() as cursor:
        try:
            result = cursor.callfunc(
                "PKG_NOTIFY_WRAP.f_update_message_status",
                oracledb.NUMBER,
                [batch_id, None, "sending"],
            )
            cursor.connection.commit()
            return result
        except oracledb.Error as e:
            logging.error(
                "Error calling PKG_NOTIFY_WRAP.f_update_message_status for batch %s: %s",
                batch_id,
                e,
            )
            cursor.connection.rollback()


def update_message_id(recipient: Recipient) -> None:
    with database.cursor() as cursor:
        try:
            cursor.execute(
                (
                    "UPDATE v_notify_message_queue "
                    "SET message_id = :message_id "
                    "WHERE nhs_number = :nhs_number"
                ),
                {
                    "message_id": recipient.message_id,
                    "nhs_number": recipient.nhs_number,
                },
            )
            cursor.connection.commit()
        except oracledb.Error as e:
            logging.error("Error updating recipient: %s", e)
            logging.error(
                "Error updating recipient %s with message ID %s: %s",
                recipient.nhs_number,
                recipient.message_id,
                e,
            )
            cursor.rollback()
