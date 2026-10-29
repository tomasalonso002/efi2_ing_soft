#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

cd src
python manage.py collectstatic --no-input
python manage.py migrate

# Crea el superusuario si definiste las variables DJANGO_SUPERUSER_* en Render.
# Como SQLite se borra en cada deploy, esto lo vuelve a crear solo.
python manage.py createsuperuser --noinput || true
