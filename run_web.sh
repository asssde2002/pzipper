#!/bin/sh

sh wait-for-postgres.sh db 5432
python manage.py migrate
python manage.py runserver 0.0.0.0:8008