from recipient import Recipient


class TestRecipient:
    def test_recipient(self):
        recipient_data = ("1234567890", "message_reference_0", "abc123", "routing_plan_id", "message_status")
        recipient = Recipient(*recipient_data)

        assert recipient.nhs_number == "1234567890"
        assert recipient.message_id == "message_reference_0"
        assert recipient.batch_id == "abc123"
        assert recipient.routing_plan_id == "routing_plan_id"
        assert recipient.message_status == "message_status"

    def test_recipient_with_partial_data(self):
        recipient_data = ("1234567890", "message_reference_0")
        recipient = Recipient(*recipient_data)

        assert recipient.nhs_number == "1234567890"
        assert recipient.message_id == "message_reference_0"
        assert recipient.batch_id is None
        assert recipient.routing_plan_id is None
        assert recipient.message_status is None

    def test_recipient_attribute_assignment(self):
        recipient_data = ("1234567890", "message_reference_0", "abc123", "routing_plan_id")
        recipient = Recipient(*recipient_data)

        recipient = recipient._replace(
            message_id="message_reference",
            message_status="message_status"
        )

        assert recipient.message_id == "message_reference"
        assert recipient.message_status == "message_status"
