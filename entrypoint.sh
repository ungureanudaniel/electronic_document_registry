#!/bin/sh

# exit immediately if a command exits with a non-zero status
set -e
# Compile Tailwind CSS
./tailwindcss-linux-x64 -i ./static/css/input.css -o ./static/css/main.css --minify

# run database migrations
echo "Running database migrations..."
python manage.py migrate

# collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting application..."
exec "$@"