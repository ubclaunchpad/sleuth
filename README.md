# Sleuth :mag_right: 
[![ZenHub](https://img.shields.io/badge/Shipping_faster_with-ZenHub-5e60ba.svg?style=flat)](https://zenhub.com)
[![Build Status](https://travis-ci.org/ubclaunchpad/sleuth.svg?branch=master)](https://travis-ci.org/ubclaunchpad/sleuth)
[![Coverage Status](https://coveralls.io/repos/github/ubclaunchpad/sleuth/badge.svg)](https://coveralls.io/github/ubclaunchpad/sleuth)

UBC's own search engine :rocket:

## Getting Started

Please see [CONTRIBUTING](https://github.com/ubclaunchpad/sleuth/blob/master/.github/CONTRIBUTING.md) for guidelines on how to contribute to this repo.

### Useful Links

Getting Started: [Docker](https://docs.docker.com/get-started/),
[Django](https://www.djangoproject.com/start/),
[Django Documentation](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/admindocs/),
[Apache Solr](https://lucene.apache.org/solr/guide/6_6/getting-started.html#getting-started),
[Haystack](https://django-haystack.readthedocs.io/en/master/tutorial.html#installation)

## Installation

- Install Docker
- Run

```Shell
$ docker-compose up
```

- Once containers have started you can `exec` into `bash` in your `web` container and configure a Django admin user.

```Shell
$ docker-compose exec web bash
# Create Django admin user
root@57d91373cdca:/home/sleuth# python3 manage.py createsuperuser
```

### Accessing Solr

- To access your Solr admin interface, go to http://localhost:8983/solr.
- To query a core with the name "test", go to http://localhost:8983/solr/#/test/query.

### Accessing Django

- The base url for your Django instance should be http://localhost:8000. 
- To access the Django admin interface make sure you have completed the steps listed above and to go http://localhost:8000/admin.

### Accessing the Sleuth Front-end App

- Go to http://localhost:8080


## Adding Test Data

Once you have started your containers you can populate the "test" core in Solr with some test data by running

```Shell
$ bash scripts/populate.sh
```