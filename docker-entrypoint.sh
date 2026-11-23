#!/bin/bash

set -e

python manage.py migrate --noinput
gunicorn -b 0.0.0.0:8000 -w 2 inultycom.wsgi:application
