#!/bin/bash

poetry run pytest -W ignore::PendingDeprecationWarning -vv tests/contract || {
    echo "Tests failed in tests/contract"
    exit 1
}