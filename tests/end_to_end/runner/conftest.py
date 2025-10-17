from contextlib import contextmanager
import dotenv
import pytest
import oracledb
import os

dotenv.load_dotenv(".env")


@pytest.fixture
def recipient_data():
    # Fixed UUIDs for reproducible tests
    return [
        ("9449304424", "e5aeb4f8-666a-cd74-0883-1caea4c3f39f"),
        ("9449305552", "966ecc3a-1e6b-5006-1ba6-f5457f496351"),
        ("9449306621", "a1b2c3d4-1234-5678-9abc-def012345678"),
        ("9449306613", "b2c3d4e5-2345-6789-abcd-ef1234567890"),
        ("9449306605", "c3d4e5f6-3456-789a-bcde-f23456789012"),
    ]


class Helpers:
    @staticmethod
    @contextmanager
    def cursor():
        conn = oracledb.connect(
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            dsn=f"{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_SID')}",
            disable_oob=True
        )
        try:
            yield conn.cursor()
        finally:
            conn.close()

    @staticmethod
    def seed_message_queue(recipient_data, message_definition_id=1):
        with Helpers.cursor() as cur:
            for nhs_number, message_id in recipient_data:
                cur.execute(
                    """
                    INSERT INTO notify_message_queue (
                        nhs_number, message_id, event_status_id, message_definition_id, message_status,
                        subject_id, event_id, pio_id
                    ) VALUES (:nhs_number, :message_id, 11197, :message_definition_id, 'new', 1, 1, 1)
                    """,
                    nhs_number=nhs_number,
                    message_id=message_id,
                    message_definition_id=message_definition_id,
                )
            cur.connection.commit()


@pytest.fixture
def helpers():
    return Helpers()


@pytest.fixture(autouse=True)
def reset_db(helpers):
    with helpers.cursor() as cur:
        cur.execute("TRUNCATE TABLE notify_message_queue")
        cur.execute("TRUNCATE TABLE notify_message_batch")
        cur.connection.commit()
