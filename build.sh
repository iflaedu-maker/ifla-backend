#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

echo "Building Django application..."

# Upgrade pip and setuptools first
pip install --upgrade pip setuptools wheel

# Install dependencies with verbose output for debugging
echo "Installing dependencies..."
pip install --upgrade --no-cache-dir -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || true

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

echo "Build completed successfully!"

