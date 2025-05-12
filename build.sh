#!/usr/bin/env bash
# exit on error
set -o errexit

# Debug info
echo "Current directory: $(pwd)"
echo "Directory listing:"
ls -la
echo "Python version: $(python --version)"

# Install dependencies
pip install -r requirements.txt

# Navigate to the project directory
cd thread_generator
echo "Project directory: $(pwd)"
echo "Directory listing:"
ls -la

# Show Python path for debugging
python -c "import sys; print('Python path:'); print('\n'.join(sys.path))"

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Create or update superuser if needed (optional)
# python manage.py createsuperuser --noinput 