FROM python:3.10-alpine

# set environment variables
ENV DJANGO_SETTINGS_MODULE=inultycom.environments.prod
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --no-cache --virtual build-deps gcc python3-dev musl-dev && \
    apk add --no-cache postgresql-dev && \
    apk add --no-cache bash

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apk add --no-cache nodejs npm
RUN npm i -g corepack && corepack enable && corepack prepare yarn@3.3.0 --activate

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN bin/build

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
