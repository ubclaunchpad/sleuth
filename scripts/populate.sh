#!/bin/bash
# Popuates Solr core "test" with sample data.
# Once this is done you can view and query your example data at http://localhost:8983/solr/#/test/query

POPULATE="post -c test example/exampledocs/*"
docker-compose exec solr sh -c "\"$POPULATE\""
