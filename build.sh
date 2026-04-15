#!/usr/bin/env bash
# Railway build script — runs once during each deploy
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
