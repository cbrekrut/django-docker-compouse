set -e

cd /app

echo "=== Применяю миграции ==="
python ScreenBook/manage.py migrate --noinput

mkdir -p /app/ScreenBook/static
chown -R appuser:appuser /app/ScreenBook/static

echo "=== Собираю static файлы ==="
python ScreenBook/manage.py collectstatic --noinput

echo "=== Запускаю Gunicorn ==="
exec gunicorn ScreenBook.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level info