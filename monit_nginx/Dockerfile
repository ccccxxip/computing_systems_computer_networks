FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    monit \
    nginx \
    curl \
    procps \
    nano \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i 's/^set daemon .*/set daemon 10/' /etc/monit/monitrc && \
    sed -i 's|^# set log /var/log/monit.log|set log /var/log/monit.log|' /etc/monit/monitrc && \
    sed -i 's/^# *set httpd/set httpd/' /etc/monit/monitrc && \
    sed -i 's/^# *use address localhost/    use address localhost/' /etc/monit/monitrc && \
    sed -i 's/^# *allow localhost/    allow localhost/' /etc/monit/monitrc && \
    sed -i 's/^# *allow admin:monit/    allow admin:monit/' /etc/monit/monitrc


COPY monit2telegram.sh /usr/local/bin/monit2telegram.sh
RUN chmod +x /usr/local/bin/monit2telegram.sh

COPY nginx.monitrc /etc/monit/conf.d/nginx
RUN chmod 600 /etc/monit/monitrc /etc/monit/conf.d/nginx

WORKDIR /root

CMD service nginx start && service monit start && bash

