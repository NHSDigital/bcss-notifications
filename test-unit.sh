#!/bin/bash

poetry run pytest --cov=src tests/unit || {
    echo "Tests failed in tests/unit"
    exit 1
}
