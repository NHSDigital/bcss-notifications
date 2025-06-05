import boto3
import csv
import functools
import os
from recipient import Recipient


@functools.cache
def get_routing_plan_id():
    return "e43a7d31-a287-485e-b1c2-f53cebbefba3"


@functools.cache
def get_recipients(batch_id: str):
    for row in csv.DictReader(raw_recipients_data()):
        yield (
            row.get("NHS_NUMBER"),
            None,
            batch_id,
            get_routing_plan_id(),
            "new",
            row.get("ADDRESS_LINE_1"),
            row.get("ADDRESS_LINE_2"),
            row.get("ADDRESS_LINE_3"),
            row.get("ADDRESS_LINE_4"),
            row.get("ADDRESS_LINE_5"),
            row.get("POSTCODE"),
        )


# pylint: disable=unused-argument
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
