FROM python:3.11.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    cron \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY . /app/
RUN chmod +x /app/run.sh
WORKDIR /app
RUN uv sync

RUN echo "*/1 * * * * /app/run.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/secretary-cron
RUN touch /var/log/cron.log
RUN chmod 0644 /etc/cron.d/secretary-cron

CMD cron && tail -f /var/log/cron.log