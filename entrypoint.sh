#!/bin/sh
set -e   # немедленно выйдем, если любая команда вернёт ненулевой код

# Убедимся, что находимся в нужной директории:
cd /app/ScreenBook

echo "=== Применяю миграции ==="
python manage.py migrate --noinput

echo "=== Собираю static файлы ==="
# В settings.py у вас должен быть STATIC_ROOT = BASE_DIR / 'static'
python manage.py collectstatic --noinput

echo "=== Запускаю Gunicorn ==="
# Gunicorn будет искать модуль ScreenBook.wsgi (файл /app/ScreenBook/ScreenBook/wsgi.py)
exec gunicorn ScreenBook.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 2 \
     --log-level info
