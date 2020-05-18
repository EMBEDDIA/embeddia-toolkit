#!/bin/bash

source activate embeddia-rest && python /var/embeddia-rest/src/manage.py migrate
source activate embeddia-rest && python /var/embeddia-rest/src/manage.py collectstatic --noinput --clear
chown www-data:www-data -R /var/embeddia-rest/static/ && chmod 777 -R /var/embeddia-rest/static/

exec "$@"
