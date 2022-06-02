#!/bin/bash

python manage.py migrate

# if [[-z "${DJANGO_USERNAME}"]];
# then
#     python manage.py createsuperuser \
#         --noinput \
#         --username $DJANGO_USERNAME \
#         --email $DJANGO_EMAIL \
#         --password $DJANGO_PASSWORD
# fi

# $@


# gunicorn --timeout=300 config.wsgi -b 0.0.0.0
python manage.py runserver 0.0.0.0:8000
