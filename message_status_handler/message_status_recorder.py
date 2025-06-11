import database


def record_message_statuses(json_data: dict):
    response_codes = []
    for data in json_data.get('data', [{}]):
        response_code = record_message_status(data)
        response_codes.append(response_code)

    return response_codes


def record_message_status(json_data: dict):
    response_code = 0
    message_reference = json_data.get('attributes', {}).get('messageReference')

    if message_reference is not None:
        with database.cursor() as cursor:
            batch_id = fetch_batch_id_for_message(cursor, message_reference)
            if batch_id is not None:
                response_code = update_message_status(cursor, batch_id, message_reference)

    return response_code


def fetch_batch_id_for_message(cursor, message_reference: str):
    cursor.execute(
        (
            "SELECT batch_id FROM v_notify_message_queue "
            "WHERE message_id = :message_reference "
            "AND message_status = 'sending'"
        ),
        {"message_reference": message_reference}
    )
    result = cursor.fetchone()

    return result[0] if result else None


def update_message_status(cursor, batch_id: str, message_reference: str):
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
