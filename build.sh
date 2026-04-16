#!/usr/bin/env bash
# build.sh — exécuté par Render lors de la construction

set -o errexit

# Installer les dépendances
pip install -r requirements.txt

# Collecter les fichiers statiques
python manage.py collectstatic --no-input

# Appliquer les migrations (base PostgreSQL fournie par DATABASE_URL)
python manage.py migrate
