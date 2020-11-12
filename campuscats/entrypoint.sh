#!/bin/sh

# In case that the database is still initalizing
echo "Waiting for MySQL..."
while ! nc -z mysql 3306; do
    sleep 0.1
done
echo "MySQL started."

# Update django things
echo "Making migrations and migrating the database."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collecting static files."
python manage.py collectstatic --noinput


exec "$@"
