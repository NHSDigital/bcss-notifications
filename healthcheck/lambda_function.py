
import access_token
import database
import environment
import logging as pylogging
import os
import requests

logging = pylogging.getLogger()
logging.setLevel("INFO")


def lambda_handler(_event, _context):
    # Environment vars from lambda and secrets manager
    logging.info("Seeding environment")
    environment.seed()
    for key in environment.KEYS:
        if os.getenv(key):
            logging.info("env var %s present", key)

    logging.info("Environment populated with secrets from secretsmanager")

    # Database check
    logging.info("Checking database connectivity")

    with database.cursor() as cursor:
        logging.info("Database connection established")
        logging.info("Executing database query")

        cursor.execute(
            """
            SELECT COUNT(*) FROM v_notify_message_queue
            """
        )
        result = cursor.fetchone()

        logging.info("Database query results (number of queued recipients): %s", result[0])
        logging.info("Database check complete")

    # OAuth check
    logging.info("OAuth2 check")
    token = access_token.get_token()
    logging.info("Access token: %s", token)

    logging.info("Communication Management API (CMAPI) check")
    response = requests.get(f"{os.getenv('COMMGT_BASE_URL')}/healthcheck", timeout=30)
    logging.info("Response from CMAPI healthcheck: %s", response.status_code)
    logging.info(response.text)
    logging.info("CMAPI check complete")

    logging.info("All checks complete")

    return {"status": "success"}
