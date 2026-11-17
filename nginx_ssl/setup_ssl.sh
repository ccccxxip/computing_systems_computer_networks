echo "127.0.0.1 superserver.net" >> /etc/hosts

mkdir -p /etc/nginx/ssl
cp nginx.crt /etc/nginx/ssl/nginx.crt
cp nginx.key /etc/nginx/ssl/nginx.key

mkdir -p /var/www/html
cp index.html /var/www/html/index.html

cp nginx_ssl.conf /etc/nginx/conf.d/superserver.conf 2>/dev/null || cp nginx_ssl.conf /etc/nginx/sites-available/default

nginx -t
service nginx restart

echo "curl -k -I https://superserver.net"
