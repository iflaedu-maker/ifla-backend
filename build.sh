#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "Building Django application..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files (including videos)
python manage.py collectstatic --noinput || true

# Verify videos are collected
echo "Checking if videos are collected..."
ls -la staticfiles/media/*.mp4 2>/dev/null || echo "Videos will be served from static/media/"

# Run migrations (skip if DATABASE_URL not set during build)
if [ -n "$DATABASE_URL" ]; then
    python manage.py migrate --noinput
else
    echo "DATABASE_URL not set, skipping migrations (will run on first start)"
fi

echo "Build completed successfully!"

