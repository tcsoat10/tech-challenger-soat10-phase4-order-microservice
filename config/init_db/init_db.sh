#!/bin/sh
set -e

# echo "Application is ready to start..." 
echo "Waiting for database to be ready..."

MAX_RETRIES=3000
COUNT=0

while ! nc -z $MYSQL_HOST $MYSQL_PORT; do
  sleep 2
  COUNT=$((COUNT+1))
  if [ $COUNT -ge $MAX_RETRIES ]; then
    echo "Database is not ready after $MAX_RETRIES attempts, exiting..."
    exit 1
  fi
done

echo "Database is up, applying migrations..."
poetry run alembic upgrade head
