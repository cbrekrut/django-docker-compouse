
set -e   
cd /app


echo "== Применяю миграции =="
python /app/ScreenBook/manage.py migrate --noinput

# 3) Собираем static
echo "== Собираю static файлы =="
python /app/ScreenBook/manage.py collectstatic --noinput

echo "== Запускаю Gunicorn =="

exec gunicorn ScreenBook.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 3 \
     --log-level info