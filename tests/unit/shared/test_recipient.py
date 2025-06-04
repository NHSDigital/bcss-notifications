from recipient import Recipient


def test_recipient():
    recipient_data = (
        "1234567890", "message_reference_0", "abc123", "routing_plan_id",
        "message_status", "address_line_1", "address_line_2",
        "address_line_3", "address_line_4", "address_line_5", "postcode"
    )
    recipient = Recipient(*recipient_data)

    assert recipient.nhs_number == "1234567890"
    assert recipient.message_id == "message_reference_0"
    assert recipient.batch_id == "abc123"
    assert recipient.routing_plan_id == "routing_plan_id"
    assert recipient.message_status == "message_status"
    assert recipient.address_line_1 == "address_line_1"
    assert recipient.address_line_2 == "address_line_2"
    assert recipient.address_line_3 == "address_line_3"
    assert recipient.address_line_4 == "address_line_4"
    assert recipient.address_line_5 == "address_line_5"
    assert recipient.postcode == "postcode"


def test_recipient_with_partial_data():
    recipient_data = ("1234567890", "message_reference_0")
    recipient = Recipient(*recipient_data)

    assert recipient.nhs_number == "1234567890"
    assert recipient.message_id == "message_reference_0"
    assert recipient.batch_id is None
    assert recipient.routing_plan_id is None
    assert recipient.message_status is None


def test_recipient_attribute_assignment():
    recipient_data = ("1234567890", "message_reference_0", "abc123", "routing_plan_id")
    recipient = Recipient(*recipient_data)

    recipient = recipient._replace(
        message_id="message_reference",
        message_status="message_status"
    )

    assert recipient.message_id == "message_reference"
    assert recipient.message_status == "message_status"
