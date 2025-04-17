FROM ghcr.io/astral-sh/uv:python3.11-alpine

WORKDIR /app

RUN apk add --no-cache \
    git \
    dcron \
    curl

COPY . /app/
RUN chmod +x /app/run.sh
WORKDIR /app
RUN uv sync

RUN echo "*/1 * * * * /app/run.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/secretary-cron
RUN touch /var/log/cron.log
RUN chmod 0644 /etc/cron.d/secretary-cron

CMD crond -f -l 8 && tail -f /var/log/cron.log