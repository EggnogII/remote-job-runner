#!/bin/sh
# Bootstrap script for running the Flask API inside a container.
#
# The container image does not assume any Python environment has
# been prepared, so this script ensures that a virtual environment
# exists, installs dependencies and then launches the API using
# that environment.

set -e

# Use the virtual environment prepared at build time.  The Dockerfile
# creates it at /venv.  When running locally we create it on the fly.
VENV_DIR="/venv"

# Create the virtual environment on first run
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install --no-cache-dir --upgrade pip
    "$VENV_DIR/bin/pip" install --no-cache-dir -r requirements.txt
fi

# Activate the environment and execute the API
. "$VENV_DIR/bin/activate"
exec "$VENV_DIR/bin/python3" ./api/index.py
