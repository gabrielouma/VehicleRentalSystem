#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python3.9 manage.py makemigrations
python3.9 manage.py migrate

# Collect static files
python3.9 manage.py collectstatic --noinput
