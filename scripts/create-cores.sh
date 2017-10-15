#!/bin/bash

set -e

bash wait.sh "Solr" "curl -s http://localhost:8983/solr"

echo "Creating cores"

for core in $@; do
     solr create -c $core
done

echo "Creating test core"

solr create_core -c test
post -c test /opt/solr/example/exampledocs/*