# syntax=docker/dockerfile:1

# --- Build JS/CSS bundle ---------------------------------------------------
FROM node:20-alpine AS assets

WORKDIR /app
RUN corepack enable

COPY package.json yarn.lock .yarnrc.yml ./
RUN yarn install --immutable

COPY rollup.config.mjs postcss.config.js tailwind.config.js ./
COPY main ./main
COPY blog ./blog
RUN yarn build


# --- App image -------------------------------------------------------------
FROM python:3.10-alpine

ENV DJANGO_SETTINGS_MODULE=inultycom.environments.prod \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN apk add --no-cache bash libpq && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

COPY . .
COPY --from=assets /app/main/static/dist ./main/static/dist

# Settings need these to import; real values are injected by Kamal at runtime.
RUN SECRET_KEY=build-only DATABASE_URL=sqlite://:memory: \
    python manage.py collectstatic --clear --no-input

RUN adduser -D -H app && chown -R app /app
USER app

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
