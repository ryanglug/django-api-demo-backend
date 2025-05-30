#!/bin/sh
set -e

# Apply database migrations
python manage.py makemigrations

python manage.py migrate

exec "$@"