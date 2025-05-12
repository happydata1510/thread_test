#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Navigate to the project directory
cd thread_generator

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Create or update superuser if needed (optional)
# python manage.py createsuperuser --noinput 