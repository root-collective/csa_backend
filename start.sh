#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Führe die Migrationen durch
pipenv run python manage.py migrate

# Samme statische Dateien
pipenv run python manage.py collectstatic --noinput

# Starte den Django-Server
# pipenv run python manage.py runserver 0.0.0.0:8000
gunicorn -c gunicorn.conf.py csa_backend.wsgi
