TELEGRAM_TOKEN="..."
TELEGRAM_CHAT_ID="..."

if [ -n "$1" ]; then
    MESSAGE_BODY="$1"
else
    MESSAGE_BODY="Служба: <b>${MONIT_SERVICE:-Nginx}</b>%0AСобытие: <b>${MONIT_EVENT:-Сбой}</b>%0AХост: <code>${MONIT_HOST:-localhost}</code>%0AОписание: ${MONIT_DESCRIPTION:-Процесс остановлен и перезапускается}"
fi

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
    -d "chat_id=${TELEGRAM_CHAT_ID}" \
    -d "text=<b>[Monit Alert]</b>%0A%0A${MESSAGE_BODY}" \
    -d "parse_mode=HTML" > /dev/null 2>&1
