# Sleuth :mag_right: [![ZenHub](https://raw.githubusercontent.com/ZenHubIO/support/master/zenhub-badge.png)](https://zenhub.com)

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

- Once containers have started you can `exec` into `bash` in your `web` container and configure a Django admin user, or run migrations.

```Shell
$ docker-compose exec web bash
# Now you should be in the web container, cd into sleuth_backend
root@57d91373cdca:/home/sleuth# cd sleuth_backend
# Run migrations
root@57d91373cdca:/home/sleuth/sleuth_backend# python3 manage.py migrate
# Start Django server
root@57d91373cdca:/home/sleuth/sleuth_backend# python3 manage.py runserver 0.0.0.0:8000
```