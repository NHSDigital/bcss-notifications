from typing import NamedTuple

# pylint: disable=unsupported-binary-operation


class Recipient(NamedTuple):
    nhs_number: str | None = None
    message_id: str | None = None
    batch_id: str | None = None
    routing_plan_id: str | None = None
    message_status: str | None = None
