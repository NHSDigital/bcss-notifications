
import access_token
import database
import environment
import logging
import os
import requests


def lambda_handler(_event, _context):
    # Environment vars from lambda and secrets manager
    logging.info("Healthcheck lambda check #1: Seeding environment from secrets manager")
    environment.seed()
    for key in environment.KEYS:
        if os.getenv(key):
            logging.info("env var %s present", key)

    logging.info("Environment populated with secrets from secretsmanager")

    # Database check
    logging.info("Healthcheck lambda #2: Checking database connectivity")

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
    logging.info("Healthcheck lambda check #3: OAuth2 check")
    token = access_token.get_token()
    logging.info("Access token obtained: %s", bool(token))

    logging.info("Healthcheck lambda check #4: Make request to NHS Notify API")
    response = requests.get(
        f"{os.getenv('NOTIFY_API_BASE_URL')}/comms/v1/messages/2WL3qFTEFM0qMY8xjRbt1LIKCzM",
        headers={"Accept": "application/vnd.api+json", "Authorization": f"Bearer {token}"},
        timeout=20
    )
    logging.info("Response from NHS Notify API: %s", response.status_code)
    logging.info(response.text)
    logging.info("NHS Notify API check complete")

    logging.info("Healthcheck lambda: All checks complete")

    return {"status": "success"}
