#!/bin/sh
set -e

source .venv/bin/activate

echo "Starting Streamlit Server"

which python

ls -la

exec "$@"
