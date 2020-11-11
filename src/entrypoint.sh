#!/bin/bash

export EMBEDDIA_API_URL="${EMBEDDIA_API_URL:-http://localhost/api/v1}"
export NLG_API_URL="${NLG_API_URL:-http://localhost:8080}"

# REST API LOCATION
sed -i "s#REST_API_URL_REPLACE#$EMBEDDIA_API_URL#g" /var/embeddia-rest/front/main*.js
# NLG API LOCATION
sed -i "s#NLG_API_URL_REPLACE#$NLG_API_URL#g" /var/embeddia-rest/front/main*.js

export EMBEDDIA_TEXTA_HOST="${EMBEDDIA_TEXTA_HOST:-https://rest-dev.texta.ee}"
export EMBEDDIA_TEXTA_TOKEN="${EMBEDDIA_TEXTA_TOKEN:-XXX}"
export EMBEDDIA_TEXTA_DASHBOARD_PROJECT="${EMBEDDIA_TEXTA_DASHBOARD_PROJECT:-247}"

# TK REST LOCATION
sed -i "s#EMBEDDIA_TEXTA_HOST#$EMBEDDIA_TEXTA_HOST#g" /var/embeddia-rest/front/main*.js
sed -i "s#EMBEDDIA_TEXTA_TOKEN#$EMBEDDIA_TEXTA_TOKEN#g" /var/embeddia-rest/front/main*.js
sed -i "s#EMBEDDIA_TEXTA_PROJECT_ID#$EMBEDDIA_TEXTA_DASHBOARD_PROJECT#g" /var/embeddia-rest/front/main*.js


source activate embeddia-rest && python /var/embeddia-rest/src/manage.py migrate
source activate embeddia-rest && python /var/embeddia-rest/src/manage.py collectstatic --noinput --clear
chown www-data:www-data -R /var/embeddia-rest/static/ && chmod 777 -R /var/embeddia-rest/static/

# NGINX CONF
sed -i "s/.*user .*www-data;.*/user www-data www-data;/" /opt/conda/envs/embeddia-rest/etc/nginx/nginx.conf
sed -i "s/^error_log .*;/error_log stderr warn;/" /opt/conda/envs/embeddia-rest/etc/nginx/nginx.conf
chown -R www-data /opt/conda/envs/embeddia-rest/var/tmp/nginx
chown -R www-data /opt/conda/envs/embeddia-rest/var/log/nginx


exec "$@"
