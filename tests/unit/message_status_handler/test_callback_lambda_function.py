import json
import callback_lambda_function as lambda_function
from unittest.mock import patch


@patch("request_verifier.verify_request")
@patch("message_status_recorder.record_message_status")
def test_lambda_handler(mock_record_message_status, mock_request_verifier):
    """Test the lambda_handler function with a valid request."""
    mock_record_message_status.return_value = 0
    mock_request_verifier.return_value = True

    event = {
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-hmac-sha256-signature": "test-signature",
            "x-api-key": "test-api-key",
            "x-correlation-id": "test-correlation-id",
        },
        "body": json.dumps(
            {
                "data": [
                    {
                        "type": "ChannelStatus",
                        "attributes": {
                            "channel": "nhsapp",
                            "supplierStatus": "read",
                            "messageId": "12345",
                        },
                    }
                ]
            }
        ),
    }

    response = lambda_function.lambda_handler(event, None)

    assert response["status"] == 200
    assert json.loads(response["body"]) == {
        "message": "Message status handler lambda finished",
        "event": event,
        "result": {"bcss_response_codes": {"0": 1, "non_zero": 0}},
    }


@patch("request_verifier.verify_request")
def test_lambda_handler_invalid_request(mock_request_verifier):
    """Test the lambda_handler function with an invalid request."""
    mock_request_verifier.return_value = False

    event = {"headers": {}, "body": json.dumps({})}

    response = lambda_function.lambda_handler(event, None)

    assert response["status"] == 200
    assert json.loads(response["body"]) == {
        "message": "Message status handler lambda finished",
        "event": event,
        "result": {},
    }


@patch("request_verifier.verify_request")
def test_lambda_handler_exception(mock_request_verifier):
    """Test the lambda_handler function when an exception occurs."""
    mock_request_verifier.side_effect = Exception("Test exception")

    event = {"headers": {}, "body": json.dumps({})}
    response = lambda_function.lambda_handler(event, None)

    assert response["status"] == 500
    assert json.loads(response["body"]) == {
        "message": "Internal Server Error: Test exception"
    }
