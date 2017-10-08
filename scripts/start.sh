#!/bin/bash
# Wait until services have booted then migrate and boot Django server

bash scripts/wait.sh "curl solr:8983/solr"
bash scripts/wait.sh "pg_isready -h db -p 5432"
python manage.py migrate
python manage.py runserver 0.0.0.0:8000