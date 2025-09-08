#!/bin/bash

# Set environment variables for production
export DJANGO_SETTINGS_MODULE=myproject.settings

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Start the application
echo "Starting Gunicorn server..."
# Use PORT environment variable if available (Azure sets this)
PORT=${PORT:-8000}
gunicorn --bind=0.0.0.0:$PORT --timeout 600 --workers 2 --worker-class gevent myproject.wsgi:application
