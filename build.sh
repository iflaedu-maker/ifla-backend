#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "Building Django application..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput || true

# Run migrations (skip if DATABASE_URL not set during build)
if [ -n "$DATABASE_URL" ]; then
    python manage.py migrate --noinput
else
    echo "DATABASE_URL not set, skipping migrations (will run on first start)"
fi

echo "Build completed successfully!"

