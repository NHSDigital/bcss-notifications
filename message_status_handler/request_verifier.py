import hashlib
import hmac
import json
import logging
import os

API_KEY_HEADER_NAME = 'x-api-key'
SIGNATURE_HEADER_NAME = 'x-hmac-sha256-signature'


def verify_request(headers: dict, body: str) -> bool:
    is_valid, error_message = verify_headers(headers)
    if not is_valid:
        logging.warning("Header verification failed: %s", error_message)
        return False

    if not verify_signature(headers, body):
        logging.warning("Signature verification failed")
        return False

    if not verify_body(json.loads(body)):
        return False

    return True


def verify_headers(headers: dict) -> tuple[bool, str]:
    lc_headers = header_keys_to_lower(headers)
    if lc_headers.get(API_KEY_HEADER_NAME) is None:
        return False, "Missing API key header"

    if lc_headers.get(API_KEY_HEADER_NAME) != notify_api_key():
        return False, "Invalid API key"

    if lc_headers.get(SIGNATURE_HEADER_NAME) is None:
        return False, "Missing signature header"

    return True, ""


def verify_signature(headers: dict, body: str) -> bool:
    lc_headers = header_keys_to_lower(headers)

    expected_signature = create_digest(signature_secret(), body)

    return hmac.compare_digest(
        expected_signature,
        lc_headers[SIGNATURE_HEADER_NAME],
    )


def verify_body(body: dict) -> bool:
    data = body.get('data', [{}])
    return all(verify_data(d) for d in data)


def verify_data(data: dict) -> bool:
    if data.get('type') == 'ChannelStatus':
        attributes = data.get('attributes', {})
        return (
            attributes.get('channel') == 'nhsapp' and
            attributes.get('supplierStatus') == 'read'
        )
    return False


def notify_api_key() -> str | None:
    return os.getenv('NOTIFY_API_KEY')


def signature_secret() -> str:
    return f"{os.getenv('APPLICATION_ID')}.{notify_api_key()}"


def header_keys_to_lower(headers: dict) -> dict:
    return {k.lower(): v for k, v in headers.items()}


def create_digest(secret: str, message: str) -> str:
    return hmac.new(
        bytes(secret, 'ASCII'),
        msg=bytes(message, 'ASCII'),
        digestmod=hashlib.sha256
    ).hexdigest()
