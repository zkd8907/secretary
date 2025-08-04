FROM ghcr.io/astral-sh/uv:python3.11-alpine

WORKDIR /app

RUN apk add --no-cache \
    git \
    curl \
    bash

COPY . /app/
RUN chmod +x /app/run.sh
WORKDIR /app
RUN uv sync

# Set default environment variables
ENV SCHEDULE_INTERVAL_MINUTES=5
ENV RUN_ON_START=false

CMD ["uv", "run", "python", "scheduler.py"]