#!/bin/bash
# Wait until services have booted before performing Django migrations.

set -e

db_ready="pg_isready -h db -p 5432"
solr_ready="curl solr:8983/solr"

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

python manage.py migrate