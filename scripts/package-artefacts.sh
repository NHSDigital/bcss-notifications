#!/bin/bash

# Define necessary variables
DOCKERFILE=create-artefacts.dockerfile

# # Create a directory for project code and virtualenv installation
PROJECT_DIR="$(realpath "$(dirname "$0")/..")"
LIB_DIR="$PROJECT_DIR/artefacts"

# Check if the pyproject.toml exists in the project directory
if [ ! -f "$PROJECT_DIR/pyproject.toml" ]; then
  echo "Error: pyproject.toml does not exist in the project directory."
  exit 1
fi

echo "pyproject.toml found at $"

# Pull the official Python 3.13 image for linux/amd64
docker build -f $DOCKERFILE --target export --output type=local,dest=./artefacts .

# Check if the export was successful
if [ -d $LIB_DIR ]; then
  echo "Python packages are successfully installed and exported to $LIB_DIR"
else
  echo "There was an error exporting the Python packages."
  exit 1
fi
