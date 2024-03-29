#!/bin/bash

set -e

# Copy static assets to volumes
rm -rf /app/static_files/*
cp -r /app/static/ /app/static_files

python manage.py migrate --noinput
gunicorn -b 0.0.0.0:8000 -w 2 inultycom.wsgi:application
