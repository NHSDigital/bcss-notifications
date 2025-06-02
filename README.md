# Bowel Cancer Screening System notifications

This repository contains a collection of serverless functions used to notify batches of recipients from the Bowel Cancer Screening System.

The functions are intended to be deployed to AWS Lambda.

## Functions

The names of the functions are a work in progress. They are described below:


### Batch Notification Processor

This function calls the BCSS Oracle database to obtain batches of recipients eligible for pre-invitation notifications.
There are currently two message definitions with corresponding notification templates designed specifically for recipients who have had a previous cancer diagnosis and for recipients with no previous diagnosis.
The batch notification processor lambda is scheduled for 08:00 and 09:00 every day. Each invocation will loop through all available batches of recipients until there are no more to process.


### Message Status Handler

This function checks the status of notifications via the Communication Management API.
It does this by fetching the batch IDs of successfully sent batches which are stored in BCSS Oracle and then fetching the message IDs of notifications delivered and read via the NHS App.
It updates the status of a batch of pre-invitations in the BCSS Oracle database.


## Development setup

### Prerequisites

- Python >= 3.11
- Docker (for local Oracle database)
- Docker compose plugin (for local Oracle database)

### Setup

Dependencies are managed using poetry. To install the dependencies and use the virtual environment, run:

```bash
pip install poetry
poetry install --no-root
```

### Environment variables

We use .env files to manage environment variables. To create a new .env file, copy the example file:

```bash
cp .env.example .env.local
```

### Oracle database container

We use a containerised Oracle database for local development and integration tests.
The development/test database connection details can be found in the .env.example file.
To start the Oracle database container, along with other development service containers run:

```bash
./start-dev-environment.sh
```


## Linting

We use pylint for linting, this can be run using the script:

```bash
./lint.sh
```

## Running the tests

We use pytest for tests, these can be run using the script:

```bash
./test-unit.sh
```

## Accessing AWS Lambda Functions via the AWS Console

This section provides a high-level overview of how to access and work with AWS Lambda functions used by the project.  
It includes guidance on which accounts to use, how to navigate the AWS Console, and tips for safely finding the correct Lambda functions.

For the full step-by-step guide, see: [How to find AWS Lambdas in the AWS Console](docs/access-aws-lambdas.md)
