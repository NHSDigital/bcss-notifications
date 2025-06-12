from contextlib import contextmanager
import dotenv
import pytest
import oracledb
import os

dotenv.load_dotenv(".env")


@pytest.fixture
def recipient_data():
    return (
        "9449304424",
        "9449305552",
        "9449306621",
        "9449306613",
        "9449306605",
    )


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
            for nhs_number in recipient_data:
                cur.execute(
                    """
                    INSERT INTO notify_message_queue (
                        nhs_number, event_status_id, message_definition_id, message_status,
                        subject_id, event_id, pio_id
                    ) VALUES (:nhs_number, 11197, :message_definition_id, 'new', 1, 1, 1)
                    """,
                    nhs_number=nhs_number,
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
