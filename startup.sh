#!/bin/bash
set -e  # Exit on error

# Set environment variables for production
export DJANGO_SETTINGS_MODULE=myproject.settings

echo "========================================"
echo "Starting Django Application Deployment"
echo "========================================"

# Create necessary directories
echo "Creating required directories..."
mkdir -p logs
mkdir -p staticfiles
mkdir -p media

# Wait for database to be ready (if using DATABASE_URL)
if [ ! -z "$DATABASE_URL" ]; then
    echo "Checking database connection..."
    python << END
import sys
import time
import dj_database_url
import psycopg2

db_config = dj_database_url.parse("$DATABASE_URL")
max_retries = 30
retry_delay = 2

for attempt in range(max_retries):
    try:
        conn = psycopg2.connect(
            dbname=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            port=db_config['PORT']
        )
        conn.close()
        print("Database connection successful!")
        sys.exit(0)
    except psycopg2.OperationalError as e:
        if attempt < max_retries - 1:
            print(f"Database not ready (attempt {attempt + 1}/{max_retries}), waiting {retry_delay}s...")
            time.sleep(retry_delay)
        else:
            print("Failed to connect to database after multiple attempts")
            sys.exit(1)
END
fi

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist (optional, for initial setup)
if [ ! -z "$DJANGO_SUPERUSER_USERNAME" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser if not exists..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
END
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Start the application
echo "========================================"
echo "Starting Gunicorn server..."
echo "========================================"

# Use PORT environment variable if available (Azure, Heroku set this)
PORT=${PORT:-8000}
WORKERS=${WORKERS:-2}
TIMEOUT=${TIMEOUT:-120}

echo "Configuration:"
echo "  Port: $PORT"
echo "  Workers: $WORKERS"
echo "  Timeout: $TIMEOUT seconds"
echo "  Worker Class: gevent"
echo ""

exec gunicorn myproject.wsgi:application \
    --bind=0.0.0.0:$PORT \
    --workers=$WORKERS \
    --worker-class=gthread \
    --threads=2 \
    --timeout=$TIMEOUT \
    --access-logfile=- \
    --error-logfile=- \
    --log-level=info \
    --capture-output
