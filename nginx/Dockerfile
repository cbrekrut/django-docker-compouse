# Используем лёгкий образ nginx
FROM nginx:1.27.0-alpine

# Удаляем стандартный конфиг, чтобы он не мешал
RUN rm /etc/nginx/conf.d/default.conf

# Копируем наш конфиг внутрь контейнера
COPY default.conf /etc/nginx/conf.d/default.conf

# Открываем порт 80
EXPOSE 80

# Запускаем nginx в foreground-режиме
CMD ["nginx", "-g", "daemon off;"]