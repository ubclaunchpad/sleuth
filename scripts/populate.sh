#!/bin/bash
# Creates a core called "test" in Solr and populates it with example data.
# Once this is done you can view and query your example data at http://localhost:8983/solr/#/test/query

CREATE_CORE="solr create_core -c test"
POPULATE="post -c test example/exampledocs/*"
docker-compose exec solr sh -c "$CREATE_CORE && $POPULATE"
