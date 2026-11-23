# syntax=docker/dockerfile:1

# --- Build JS/CSS bundle ---------------------------------------------------
FROM node:24-alpine AS assets

WORKDIR /app
RUN corepack enable

COPY package.json yarn.lock .yarnrc.yml ./
RUN yarn install --immutable

COPY rollup.config.mjs postcss.config.js tailwind.config.js ./
COPY main ./main
COPY blog ./blog
RUN yarn build


# --- App image -------------------------------------------------------------
FROM python:3.13-alpine

# Same uv version as .mise.toml
COPY --from=ghcr.io/astral-sh/uv:0.13.9 /uv /usr/local/bin/uv

ENV DJANGO_SETTINGS_MODULE=inultycom.environments.prod \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install exactly what uv.lock pins (no dev deps) into /app/.venv, using the
# image's Python. Only re-runs when the lockfile changes.
COPY pyproject.toml uv.lock ./
RUN apk add --no-cache bash libpq && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    uv sync --locked --no-dev --no-cache && \
    apk del .build-deps

COPY . .
COPY --from=assets /app/main/static/dist ./main/static/dist

# Settings need these to import; real values are injected by Kamal at runtime.
RUN SECRET_KEY=build-only DATABASE_URL=sqlite://:memory: \
    python manage.py collectstatic --clear --no-input

# Runs unprivileged; /app stays root-owned and read-only to the app.
RUN adduser -D app
USER app

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
