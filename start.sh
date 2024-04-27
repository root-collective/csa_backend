#!/bin/bash

# Führe die Migrationen durch
pipenv run python manage.py migrate

# Starte den Django-Server
pipenv run python manage.py runserver 0.0.0.0:8000