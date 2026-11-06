set -e
if [ "$EUID" -ne 0 ]; then
  echo "Запустите скрипт с правами суперпользователя: sudo bash setup.sh"
  exit 1
fi

echo "Копирование скрипта оповещений в /usr/local/bin/monit2telegram.sh..."
cp monit2telegram.sh /usr/local/bin/monit2telegram.sh
chmod +x /usr/local/bin/monit2telegram.sh

echo "Копирование конфигурации Nginx в /etc/monit/conf.d/nginx..."
mkdir -p /etc/monit/conf.d/
cp nginx.monitrc /etc/monit/conf.d/nginx

echo "Настройка интервала опроса Monit (10 секунд)..."
sed -i 's/^set daemon .*/set daemon 10/' /etc/monit/monitrc 2>/dev/null || true

echo "Проверка корректности синтаксиса Monit..."
monit -t

echo "Перезапуск Monit..."
systemctl restart monit || service monit restart
monit reload || true

echo "Установка завершена успешно!"
echo "Проверьте статус командой: sudo monit status"

