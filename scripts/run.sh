#!/bin/sh

set -e

whoami

python manage.py

uwsgi --socket :9000 --workers 4 --master --enable-threads --module core.wsgi