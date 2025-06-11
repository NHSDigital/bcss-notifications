import boto3
import csv
import functools
import os
import uuid
from recipient import Recipient


# pylint: disable=unused-argument

@functools.cache
def get_routing_plan_id(batch_id: str):
    return "e43a7d31-a287-485e-b1c2-f53cebbefba3"


@functools.cache
def get_recipients(batch_id: str):
    recipients = []

    if not bool(os.getenv("TEST_DATA_FETCHED")):
        for row in csv.DictReader(raw_recipients_data()):
            recipients.append(
                Recipient((
                    row.get("NHS_NUMBER"),
                    str(uuid.uuid4()),
                    batch_id,
                    get_routing_plan_id(batch_id),
                    "new",
                    row.get("ADDRESS_LINE_1"),
                    row.get("ADDRESS_LINE_2"),
                    row.get("ADDRESS_LINE_3"),
                    row.get("ADDRESS_LINE_4"),
                    row.get("ADDRESS_LINE_5"),
                    row.get("POSTCODE"),
                ))
            )
        os.environ["TEST_DATA_FETCHED"] = "true"

    return recipients


def mark_batch_as_sent(batch_id: str):
    return 1


def update_message_id(recipient: Recipient):
    return True


@functools.cache
def raw_recipients_data():
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
    )
    response = s3_client.get_object(Bucket=os.getenv("AWS_S3_BUCKET"), Key="test-recipients.csv")

    status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

    data = []

    if status == 200:
        print(f"Successful S3 get_object response. Status - {status}")
        data = response['Body'].read().decode('utf-8').splitlines()
    else:
        print(f"Unsuccessful S3 get_object response. Status - {status}")

    return data
