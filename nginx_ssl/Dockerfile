FROM nginx:alpine

RUN mkdir -p /etc/nginx/ssl /var/www/html

COPY nginx_ssl.conf /etc/nginx/conf.d/default.conf
COPY nginx.crt /etc/nginx/ssl/nginx.crt
COPY nginx.key /etc/nginx/ssl/nginx.key
COPY index.html /var/www/html/index.html

EXPOSE 80 443
