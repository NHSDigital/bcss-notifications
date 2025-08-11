import database
from oracledb import Cursor
import logging


def record_message_statuses(json_data: dict) -> dict[str, int]:
    response_counts = {"zero": 0, "non_zero": 0}

    for data in json_data.get("data", []):
        response_code = record_message_status(data)
        if response_code == 0:
            response_counts["zero"] += 1
        else:
            response_counts["non_zero"] += 1

    return response_counts


def record_message_status(json_data: dict) -> int:
    response_code = 0
    message_reference = json_data.get("attributes", {}).get("messageReference")

    if message_reference is not None:
        with database.cursor() as cursor:
            batch_id = fetch_batch_id_for_message(cursor, message_reference)
            if batch_id is not None:
                response_code = update_message_status(
                    cursor, batch_id, message_reference
                )
            else:
                logging.error("Cannot update status of message %s", message_reference)

    if response_code > 0:
        logging.error(
            "Error updating status of message %s - oracle error ID %s",
            message_reference,
            response_code,
        )

    return response_code


def fetch_batch_id_for_message(cursor: Cursor, message_reference: str) -> str | None:
    cursor.execute(
        (
            "SELECT batch_id FROM v_notify_message_queue "
            "WHERE message_id = :message_reference "
            "AND message_status = 'sending'"
        ),
        {"message_reference": message_reference},
    )
    result = cursor.fetchone()

    return result[0] if result else None


def update_message_status(cursor: Cursor, batch_id: str, message_reference: str) -> int:
    var = cursor.var(int)

    cursor.execute(
        """
            begin
                :out_val := pkg_notify_wrap.f_update_message_status(:in_val1, :in_val2, :in_val3);
            end;
        """,
        {
            "in_val1": batch_id,
            "in_val2": message_reference,
            "in_val3": "read",
            "out_val": var,
        },
    )
    cursor.connection.commit()

    return var.getvalue()
