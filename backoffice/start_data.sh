#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/customers.json
python manage.py loaddata fixtures/supermarkets.json
python manage.py runserver 0.0.0.0:8000