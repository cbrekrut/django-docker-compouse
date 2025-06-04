FROM nginx:1.27.0-alpine

# Удалим дефолтный конфиг, чтобы он не мешал
RUN rm /etc/nginx/conf.d/default.conf

# Копируем ваш конфиг
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

