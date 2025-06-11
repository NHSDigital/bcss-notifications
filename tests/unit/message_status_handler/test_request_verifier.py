import request_verifier
import json
import pytest
from unittest.mock import Mock


@pytest.fixture(autouse=True)
def setup(monkeypatch):
    """Set up environment variables for tests."""
    monkeypatch.setenv('APPLICATION_ID', 'application_id')
    monkeypatch.setenv('API_KEY', 'api_key')


def test_verify_signature_invalid():
    """Test that an invalid signature fails verification."""
    headers = {request_verifier.SIGNATURE_HEADER_NAME: 'signature'}
    body = {'data': [{'body': 'valid'}]}

    assert not request_verifier.verify_signature(headers, body)


def test_verify_signature_valid():
    """Test that a valid signature passes verification."""
    body = {'data': [{'body': 'valid'}]}
    signature = request_verifier.create_digest('application_id.api_key', json.dumps(body))

    headers = {request_verifier.SIGNATURE_HEADER_NAME: signature}
    assert request_verifier.verify_signature(headers, body)


def test_verify_headers_missing_all():
    """Test that missing all headers fails verification."""
    headers = {}
    assert request_verifier.verify_headers(headers) == (False, 'Missing API key header')


def test_verify_headers_missing_api_key():
    """Test that missing API key header fails verification."""
    headers = {request_verifier.SIGNATURE_HEADER_NAME: 'signature'}
    assert request_verifier.verify_headers(headers) == (False, 'Missing API key header')


def test_verify_headers_missing_signature():
    """Test that missing signature header fails verification."""
    headers = {request_verifier.API_KEY_HEADER_NAME: 'api_key'}
    assert request_verifier.verify_headers(headers) == (False, 'Missing signature header')


def test_verify_headers_valid():
    """Test that valid API key and signature headers pass verification."""
    headers = {
        request_verifier.API_KEY_HEADER_NAME: 'api_key',
        request_verifier.SIGNATURE_HEADER_NAME: 'signature',
    }
    assert request_verifier.verify_headers(headers)


def test_verify_headers_invalid_api_key():
    """Test that an invalid API key fails verification."""
    headers = {request_verifier.API_KEY_HEADER_NAME: 'invalid_api_key'}
    assert request_verifier.verify_headers(headers) == (False, 'Invalid API key')


def test_verify_body_invalid_type():
    """Test that an invalid body type fails verification."""
    body = {'data': [{'type': 'InvalidType', 'attributes': {}}]}
    assert not request_verifier.verify_body(body)


def test_verify_body_invalid_attributes():
    """Test that an invalid body attributes fails verification."""
    body = {'data': [{'type': 'ChannelStatus', 'attributes': {'channel': 'nhsapp', 'supplierStatus': 'unread'}}]}
    assert not request_verifier.verify_body(body)


def test_verify_body_valid():
    """Test that a valid body passes verification."""
    body = {'data': [{'type': 'ChannelStatus', 'attributes': {'channel': 'nhsapp', 'supplierStatus': 'read'}}]}
    assert request_verifier.verify_body(body)


def test_verify_request_invalid_headers():
    """Test that invalid headers fail request verification."""
    headers = {request_verifier.API_KEY_HEADER_NAME: 'invalid_api_key'}
    body = {'data': [{'type': 'ChannelStatus', 'attributes': {'channel': 'nhsapp', 'supplierStatus': 'read'}}]}

    assert not request_verifier.verify_request(headers, body)


def test_verify_request_for_valid_request():
    """Test that a valid request passes verification."""
    request_verifier.verify_headers = Mock(return_value=(True, ''))
    request_verifier.verify_signature = Mock(return_value=True)
    request_verifier.verify_body = Mock(return_value=True)

    headers = {
        request_verifier.API_KEY_HEADER_NAME: 'api_key',
        request_verifier.SIGNATURE_HEADER_NAME: 'signature',
    }

    body = {'data': [{'type': 'ChannelStatus', 'attributes': {'channel': 'nhsapp', 'supplierStatus': 'read'}}]}

    assert request_verifier.verify_request(headers, body) is True
