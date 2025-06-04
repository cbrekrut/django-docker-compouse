#!/bin/sh
set -e

cd /app/ScreenBook

echo "=== Применяю миграции ==="
python manage.py migrate --noinput

echo "=== Создаю суперпользователя (если ещё нет) ==="
python <<EOF
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScreenBook.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
email = 'admin@example.com'
password = '123456'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Суперпользователь '{username}' создан.")
else:
    print(f"Суперпользователь '{username}' уже существует.")
EOF

echo "=== Собираю static-файлы ==="
python manage.py collectstatic --noinput

echo "=== Запускаю Gunicorn ==="
exec gunicorn ScreenBook.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 3 \
     --log-level info
