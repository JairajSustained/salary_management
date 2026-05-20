#!/bin/sh
set -e

echo "Running migrations…"
uv run python manage.py migrate --no-input

echo "Starting server…"
exec uv run python manage.py runserver 0.0.0.0:8000
