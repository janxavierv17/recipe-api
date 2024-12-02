#!/bin/sh

# Exit immediately if any command exits with a non-zero status
set -e

# Wait for the database to be ready before proceeding
python manage.py wait_for_db

# Collect static files without prompting for input
python manage.py collectstatic --no-input

# Apply database migrations
python manage.py migrate

# Start the uWSGI server
# --socket :9000     Exposes a TCP socket on port 9000 for Nginx to connect to the application
# --workers 4        Spawns 4 worker processes to handle requests
# --master           Runs uWSGI as a master process
# --enable-threads   Enables threading in the workers
# --module app.wsgi  Specifies the WSGI module to run (app/wsgi.py in this case)
uwsgi --socket :9000 --workers 4 --master --enable-threads --module app.wsgi
