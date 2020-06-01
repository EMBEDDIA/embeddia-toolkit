#!/bin/bash
set -xe
: "${EMBEDDIA_API_URL?Need an api url}"

sed -i "s#REST_API_URL_REPLACE#$EMBEDDIA_API_URL#g" /usr/share/nginx/html/main*.js

exec "$@"
