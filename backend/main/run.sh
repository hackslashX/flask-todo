#! /usr/bin/env bash

# Perform pre-start checks
. prestart.sh

export APP_MODULE=${APP_MODULE-main:app}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-5000}

# run gunicorn
exec gunicorn --bind $HOST:$PORT "$APP_MODULE" --log-level DEBUG