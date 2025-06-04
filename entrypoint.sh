#!/bin/sh
set -e

cd /app/ScreenBook

echo "=== Применяю миграции ==="
python manage.py migrate --noinput

echo "=== Создаю суперпользователя (по email) ==="
python <<EOF
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScreenBook.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Значения для суперпользователя:
email = 'admin@example.com'
password = '123456'
first_name = 'Admin'   # если у вашей модели есть эти поля и они обязательны
last_name = 'User'

# Поскольку у вас для входа используется email, просто проверяем по полю 'email':
if not User.objects.filter(email=email).exists():
    # create_superuser при этом должен вызываться так:
    User.objects.create_superuser(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    print(f"Суперпользователь '{email}' создан.")
else:
    print(f"Суперпользователь '{email}' уже существует.")
EOF

echo "=== Собираю static-файлы ==="
python manage.py collectstatic --noinput

echo "=== Запускаю Gunicorn ==="
exec gunicorn ScreenBook.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 3 \
     --log-level info