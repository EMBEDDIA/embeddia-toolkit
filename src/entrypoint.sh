#!/bin/bash

source activate embeddia-rest && python manage.py migrate
source activate embeddia-rest && python manage.py collectstatic --noinput --clear
chown www-data:www-data -R /var/embeddia-rest/static/ && chmod 777 -R /var/embeddia-rest/static/

set | egrep "^(DJANGO|TEXTA|PYTHON|LC_|LANG)" | sed -e 's/^/export /' > .env

exec "$@"
