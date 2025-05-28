from typing import NamedTuple

# pylint: disable=unsupported-binary-operation


class Recipient(NamedTuple):
    nhs_number: str | None = None
    message_id: str | None = None
    batch_id: str | None = None
    routing_plan_id: str | None = None
    message_status: str | None = None
    variable_text_1: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    address_line_3: str | None = None
    address_line_4: str | None = None
    address_line_5: str | None = None
    postcode: str | None = None
    gp_practice_name: str | None = None
