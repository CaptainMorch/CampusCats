#!/bin/sh

# In case that the database is still initalizing
echo "Waiting for MySQL..."
while ! nc -z mysql 3306; do
    sleep 1
done
echo "MySQL started."

# Update django things
echo "Try migrating the database."
python manage.py migrate --noinput

echo "Collecting static files."
python manage.py collectstatic --noinput

# Starting server
echo "Strating gunicorn server."
gunicorn campuscats.wsgi -c /run/secrets/gunicorn.conf.py

exec "$@"
