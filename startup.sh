#!/bin/bash

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate --noinput

# Start the application
gunicorn --bind=0.0.0.0 --timeout 600 myproject.wsgi
