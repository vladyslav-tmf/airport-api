#!/bin/sh
set -e

# Script to initialize and start the Django application

# Print waiting message and connection details
echo "Waiting for postgres..."
echo $POSTGRES_HOST
echo $POSTGRES_PORT

# Wait for PostgreSQL to be ready by checking connection
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

# Notify that PostgreSQL is available
echo "PostgreSQL started"

# Run database migrations
make migrate

# Execute the main command passed to the container
exec "$@"
