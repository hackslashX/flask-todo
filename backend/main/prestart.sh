#! /usr/bin/env bash

# Let the DB start
python /todo/app/db/health_check.py

# Run migrations
alembic upgrade head