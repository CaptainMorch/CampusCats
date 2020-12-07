#!/bin/sh

echo "Waiting for MySQL service..."
while ! nc -z mysql 3306; do
    sleep 1
done
echo "MySQL started."

exit 0