python manage.py migrate --no-input
python manage.py collectstatic --no-input
DJANGO_SUPERUSER_PASSWORD=admin python manage.py createsuperuser --username admin --email admin@admin.com --noinput

gunicorn django_project.wsgi:application --bind 0.0.0.0:8000