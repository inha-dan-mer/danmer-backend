#!/bin/bash

python manage.py migrate


# gunicorn --timeout=300 config.wsgi -b 0.0.0.0
python manage.py runserver 0.0.0.0:8000
