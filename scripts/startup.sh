#!/bin/bash
# Wait until services have booted before performing Django migrations and running 
# the server.

set -e

db_ready="pg_isready -h db -p 5432"
solr_ready="curl solr:8983/solr"
migrate="python manage.py migrate"
run_server="python manage.py runserver 0.0.0.0:8000"

>&2 echo "Waiting for Solr to boot"
until $solr_ready; do
  sleep 10
done
>&2 echo "Solr ready"

>&2 echo "Waiting for Postgres to boot"
until $db_ready; do
  sleep 5
done
>&2 echo "Postgres ready"

$migrate && $run_server
>&2 echo "ALL SERVICES ARE READY!"