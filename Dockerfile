# Verwende Ubuntu als Basisimage
FROM ubuntu:jammy

# Setze Arbeitsverzeichnis im Container
WORKDIR /app

# Aktualisiere das Paketverzeichnis und installiere grundlegende Tools
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install pipenv

# Kopiere Pipfile und Pipfile.lock in den Container
COPY Pipfile Pipfile.lock ./

# Installiere Abhängigkeiten mit pipenv
RUN pipenv install --deploy --ignore-pipfile

# Kopiere den Rest des Codes in den Container
COPY . .

# Exponiere den Port, den Django verwenden wird (Standardmäßig 8000)
EXPOSE 8000

# Führe das Django-Projekt
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
