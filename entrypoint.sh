#!/bin/bash
set -e

echo "Waiting for MySQL at ${MYSQL_HOST:-db}:${MYSQL_PORT:-3306}..."
until python -c "import os, MySQLdb; MySQLdb.connect(host=os.environ.get('MYSQL_HOST','db'), port=int(os.environ.get('MYSQL_PORT',3306)), user=os.environ.get('MYSQL_USER','chef_user'), passwd=os.environ.get('MYSQL_PASSWORD','chef_pass_fiji'), db=os.environ.get('MYSQL_DATABASE','chefs_garden_fiji'))" 2>/dev/null; do
    echo "MySQL is unavailable - sleeping 2s"
    sleep 2
done

echo "MySQL is up! Running migrations..."
python manage.py makemigrations catalog --noinput
python manage.py migrate --noinput

echo "Seeding initial Chefs Garden Fiji catalog and admin user..."
python manage.py seed_catalog

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Chefs Garden Fiji server on 0.0.0.0:8000..."
exec gunicorn chefs_garden.wsgi:application --bind 0.0.0.0:8000 --workers 3 --reload
