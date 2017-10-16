#!/bin/bash
#
# docker-entrypoint for docker-solr

set -e

echo "Starting Solr"

solr -f & 
bash create-cores.sh $@ &
wait