#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

cd src
python manage.py collectstatic --no-input
python manage.py migrate

# Crear superusuario de forma segura con Python
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
username = '$DJANGO_SUPERUSER_USERNAME'
email = '$DJANGO_SUPERUSER_EMAIL'
password = '$DJANGO_SUPERUSER_PASSWORD'

if not User.objects.filter(**{User.USERNAME_FIELD: username}).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superusuario creado correctamente.')
else:
    print('El superusuario ya existe.')
"
fi
