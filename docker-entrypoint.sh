#!/bin/bash

set -e

# Copy nginxconfig and static assets to volumes
cp /app/nginx/inultycom-nginx.conf /app/nginx_conf/inultycom-nginx.conf
cp -r /app/static/ /app/static_files

python manage.py migrate --noinput
gunicorn -b 0.0.0.0:8000 -w 2 inultycom.wsgi:application
