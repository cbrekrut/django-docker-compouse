#!/bin/sh
set -e

# Переходим в папку, где лежит manage.py и пакет ScreenBook
cd /app/ScreenBook

echo "=== Применяю миграции ==="
python manage.py migrate --noinput

echo "=== Собираю static файлы ==="
python manage.py collectstatic --noinput

echo "=== Запускаю Gunicorn ==="
exec gunicorn ScreenBook.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 3 \
     --log-level info