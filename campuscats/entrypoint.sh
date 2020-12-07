#!/bin/sh
set -o errexit

# In case that the database is still initalizing
bash ./wait-for-mysql.sh

# Update django things
echo "Try migrating the database."
python manage.py migrate --noinput

echo "Collecting static files."
python manage.py collectstatic --noinput

# Starting server
echo "Strating gunicorn server."
gunicorn campuscats.wsgi -c settings/gunicorn.conf.py

exec "$@"
