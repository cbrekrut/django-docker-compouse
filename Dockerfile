FROM python:3.11-alpine AS base

ENV PYTHONUNBUFFERED=1

RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev jpeg-dev zlib-dev postgresql-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh

RUN addgroup -S appuser && adduser -S appuser -G appuser
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000


ENTRYPOINT ["/app/entrypoint.sh"]
