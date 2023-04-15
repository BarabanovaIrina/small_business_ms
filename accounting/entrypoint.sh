#!/bin/sh
APP_PORT=${PORT:-8003}
cd /app/
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm accounting.wsgi:application --bind "0.0.0.0:${APP_PORT}"
