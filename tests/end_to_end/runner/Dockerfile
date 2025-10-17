# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.13-bullseye AS builder

ENV APPLICATION_ID=${APPLICATION_ID} \
    DATABASE_USER=${DATABASE_USER} \
    DATABASE_PASSWORD=${DATABASE_PASSWORD} \ 
    DATABASE_SID=${DATABASE_SID} \
    DATABASE_HOST=${DATABASE_HOST} \
    DATABASE_PORT=${DATABASE_PORT} \
    NOTIFY_API_BASE_URL=${NOTIFY_API_BASE_URL} \
    NOTIFY_API_KEY=${NOTIFY_API_KEY} \
    OAUTH_API_KID=${OAUTH_API_KID} \
    OAUTH_API_KEY=${OAUTH_API_KEY} \
    OAUTH_TOKEN_URL=${OAUTH_TOKEN_URL} \
    PIP_ONLY_BINARY=ALL \
    PRIVATE_KEY=${PRIVATE_KEY} \
    REGION_NAME=${REGION_NAME}

COPY --from=root_dir pyproject.toml /
COPY --from=root_dir poetry.lock /
COPY --from=root_dir .env.test /.env
COPY --from=root_dir message_status_handler/request_verifier.py /tests/end_to_end/request_verifier.py
COPY --from=root_dir shared/exceptions.py /tests/end_to_end/exceptions.py
COPY . /tests/end_to_end

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
