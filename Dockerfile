# ─────────────────────────────────────────────────────────────────────────────
# 1) Базовый образ и системные зависимости
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev jpeg-dev zlib-dev postgresql-dev

# ─────────────────────────────────────────────────────────────────────────────
# 2) Создаём непривилегированного пользователя
# ─────────────────────────────────────────────────────────────────────────────
RUN addgroup -S appuser && adduser -S appuser -G appuser

# ─────────────────────────────────────────────────────────────────────────────
# 3) Устанавливаем зависимости Python
# ─────────────────────────────────────────────────────────────────────────────
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Делаем entrypoint.sh исполняемым
RUN chmod +x /app/entrypoint.sh

# Передаём права папке /app непривилегированному пользователю
RUN chown -R appuser:appuser /app
USER appuser

# ─────────────────────────────────────────────────────────────────────────────
# 5) Открываем порт 8000 (Gunicorn)
# ─────────────────────────────────────────────────────────────────────────────
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
