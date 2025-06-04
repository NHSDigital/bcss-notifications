import communication_management
from recipient import Recipient
import pytest
import requests_mock
from unittest.mock import patch


@pytest.fixture(autouse=True)
def setup(monkeypatch):
    monkeypatch.setenv("COMMGT_BASE_URL", "http://example.com")
    monkeypatch.setenv("APPLICATION_ID", "application_id")
    monkeypatch.setenv("API_KEY", "api_key")


@patch("access_token.get_token", return_value="access_token")
def test_send_batch_message(mock_get_token):
    with requests_mock.Mocker() as rm:
        adapter = rm.post(
            "http://example.com/message/batch",
            status_code=201,
            json={"data": {"id": "batch_id"}},
        )

        communication_management.send_batch_message(
            "batch_id",
            "routing_config_id",
            [
                Recipient(
                    "0000000000", "message_reference_0", "batch_id_0", "requested",
                    "routing_config_id_0", "address_line_01", "address_line_02",
                    "address_line_03", "address_line_04", "address_line_05", "postcode_0"
                ),
                Recipient(
                    "1111111111", "message_reference_1", "batch_id_1", "requested",
                    "routing_config_id_1", "address_line_11", "address_line_12",
                    "address_line_13", "address_line_14", "address_line_15", "postcode_1"
                ),
            ]
        )
        assert adapter.last_request.url == "http://example.com/message/batch"
        assert adapter.last_request.headers["x-api-key"] == "api_key"
        assert adapter.last_request.headers["authorization"] == "Bearer access_token"
        assert adapter.last_request.json() == {
            "data": {
                "type": "MessageBatch",
                "attributes": {
                    "routingPlanId": "routing_config_id",
                    "messageBatchReference": "batch_id",
                    "messages": [
                        {
                            "recipient": {"nhsNumber": "0000000000"},
                            "messageReference": "message_reference_0",
                            "personalisation": {
                                "address_line_1_bcss": "address_line_01",
                                "address_line_2_bcss": "address_line_02",
                                "address_line_3_bcss": "address_line_03",
                                "address_line_4_bcss": "address_line_04",
                                "address_line_5_bcss": "address_line_05",
                                "address_line_6_bcss": "postcode_0",
                            },
                        },
                        {
                            "recipient": {"nhsNumber": "1111111111"},
                            "messageReference": "message_reference_1",
                            "personalisation": {
                                "address_line_1_bcss": "address_line_11",
                                "address_line_2_bcss": "address_line_12",
                                "address_line_3_bcss": "address_line_13",
                                "address_line_4_bcss": "address_line_14",
                                "address_line_5_bcss": "address_line_15",
                                "address_line_6_bcss": "postcode_1",
                            },
                        },
                    ],
                },
            },
        }


def test_generate_batch_message_request_body():
    recipients = [
        Recipient("0000000000", "message_reference_0", "requested"),
        Recipient("1111111111", "message_reference_1", "requested"),
    ]

    message_batch = communication_management.generate_batch_message_request_body("routing_config_id", "batch_reference", recipients)

    assert message_batch["data"]["attributes"]["routingPlanId"] == "routing_config_id"
    assert message_batch["data"]["attributes"]["messageBatchReference"] == "batch_reference"
    assert len(message_batch["data"]["attributes"]["messages"]) == 2
    assert message_batch["data"]["attributes"]["messages"][0]["recipient"]["nhsNumber"] == "0000000000"
    assert message_batch["data"]["attributes"]["messages"][0]["messageReference"] == "message_reference_0"
    assert message_batch["data"]["attributes"]["messages"][1]["recipient"]["nhsNumber"] == "1111111111"
    assert message_batch["data"]["attributes"]["messages"][1]["messageReference"] == "message_reference_1"


def test_generate_message():
    recipient = Recipient(
        "0000000000", "message_reference_0", "batch_id_0", "requested",
        "routing_config_id_0", "address_line_01", "address_line_02",
        "address_line_03", "address_line_04", "address_line_05", "postcode_0"
    )

    message = communication_management.generate_message(recipient)

    assert message["messageReference"] == "message_reference_0"
    assert message["recipient"]["nhsNumber"] == "0000000000"
    assert message["personalisation"] == {
        "address_line_1_bcss": "address_line_01",
        "address_line_2_bcss": "address_line_02",
        "address_line_3_bcss": "address_line_03",
        "address_line_4_bcss": "address_line_04",
        "address_line_5_bcss": "address_line_05",
        "address_line_6_bcss": "postcode_0",
    }


def test_generate_hmac_signature():
    hmac_signature = communication_management.generate_hmac_signature({"data": "data"})

    assert hmac_signature == "e2a0ce7f9e78746d86cbdb5ebcc9bae6eb25bfed844498d3f818ae5f975ef40f"


def test_get_read_messages(monkeypatch):
    monkeypatch.setenv("COMMGT_BASE_URL", "http://example.com")

    with requests_mock.Mocker() as rm:
        adapter = rm.get(
            "http://example.com/statuses",
            status_code=201,
            json={
                'status': 'success',
                'response': 'message_batch_post_response',
                'data': [{
                    'channel': 'nhsapp',
                    'channelStatus': 'delivered',
                    'supplierStatus': 'read',
                    'message_id': '2WL3qFTEFM0qMY8xjRbt1LIKCzM',
                    'message_reference': '1642109b-69eb-447f-8f97-ab70a74f5db4'
                }]
            }
        )

        response_json = communication_management.get_read_messages("c3b8e0c4-5f3d-4a2b-8c7f-1a2e9d6f3b5c")

        assert response_json["status"] == "success"
        assert len(response_json["data"]) == 1
        assert response_json["data"][0]["channel"] == "nhsapp"
        assert response_json["data"][0]["channelStatus"] == "delivered"
        assert response_json["data"][0]["supplierStatus"] == "read"
        assert response_json["data"][0]["message_id"] == "2WL3qFTEFM0qMY8xjRbt1LIKCzM"
        assert response_json["data"][0]["message_reference"] == "1642109b-69eb-447f-8f97-ab70a74f5db4"

        assert adapter.called
        assert adapter.call_count == 1
        assert adapter.last_request.qs == {
            "batchreference": ["c3b8e0c4-5f3d-4a2b-8c7f-1a2e9d6f3b5c"],
            "channel": ["nhsapp"],
            "supplierstatus": ["read"],
        }


def test_get_read_messages_no_data(monkeypatch):
    monkeypatch.setenv("COMMGT_BASE_URL", "http://example.com")

    with requests_mock.Mocker() as rm:
        rm.get(
            "http://example.com/statuses",
            status_code=201,
            json={
                'status': 'success',
                'data': []
            }
        )

        response_json = communication_management.get_read_messages("c3b8e0c4-5f3d-4a2b-8c7f-1a2e9d6f3b5c")

        assert response_json["status"] == "success"
        assert response_json["data"] == []


def test_get_read_messages_exception(monkeypatch):
    monkeypatch.setenv("COMMGT_BASE_URL", "http://example.com")

    with requests_mock.Mocker() as rm:
        rm.get(
            "http://example.com/statuses",
            status_code=500,
            json={
                'status': 'error',
                'data': []
            }
        )

        response_json = communication_management.get_read_messages("c3b8e0c4-5f3d-4a2b-8c7f-1a2e9d6f3b5c")

        assert response_json["status"] == "error"
        assert response_json["data"] == []
