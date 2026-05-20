#!/bin/sh
set -e

echo "Running migrations…"
uv run python manage.py migrate --no-input

echo "Starting server…"
exec uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2