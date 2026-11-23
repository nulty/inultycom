# Local tasks. Server-side tasks are Kamal aliases (config/deploy.yml):
#   kamal logs | shell | manage <cmd> | dbc | dblogs

# Use mise's environment (pinned tools + ./.venv first on PATH) for every recipe and
# everything it starts (foreman, bin/ scripts), even outside an activated shell.
export PATH := $(shell mise exec -- printenv PATH)

SITE      := https://inulty.com
SERVER    := root@178.128.165.170
# Key comes from ~/.ssh/config (see config/deploy.yml)
SSH       := ssh $(SERVER)
PY        := python
YARN      := COREPACK_ENABLE_DOWNLOAD_PROMPT=0 corepack yarn
DEV       := DJANGO_SETTINGS_MODULE=inultycom.environments.dev
# Enough env for prod settings to load without a real database
CHECK_ENV := DJANGO_SETTINGS_MODULE=inultycom.environments.prod SECRET_KEY=check-only-not-a-real-key-0123456789abcdefghijklmnopqrstuvwxyz \
             DATABASE_URL=sqlite://:memory: ALLOWED_HOSTS=inulty.com

.DEFAULT_GOAL := help
.PHONY: help setup dev superuser assets check test image smoke smoke-live deploy backup outdated upgrade

help: ## List tasks
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  \033[36m%-11s\033[0m %s\n", $$1, $$2}'

setup: ## Install tools, Python deps (uv, from uv.lock) and JS deps, build assets, migrate local DB
	mise install
	uv sync --locked
	$(YARN) install
	$(YARN) build
	$(DEV) $(PY) manage.py migrate

dev: ## Run dev server on :8000, livereload and asset watcher (foreman)
	$(DEV) $(PY) manage.py migrate --no-input
	bin/foreman

superuser: ## Create a local admin user (for previewing drafts)
	$(DEV) $(PY) manage.py createsuperuser

assets: ## Build the JS/CSS bundle
	$(YARN) build

check: ## Django system checks + missing migrations, against prod settings
	$(CHECK_ENV) $(PY) -Wd manage.py check --deploy --fail-level ERROR
	$(CHECK_ENV) $(PY) manage.py makemigrations --check --dry-run

test: ## Run the Django test suite (SQLite in memory)
	$(CHECK_ENV) $(PY) manage.py test

image: ## Build the production Docker image
	docker build --platform linux/amd64 -t inultycom .

smoke: ## Build the image and smoke test it against a throwaway Postgres
	bin/smoke

smoke-live: ## Smoke test the live site
	bin/smoke $(SITE)

deploy: check test smoke ## Check, test, smoke test, deploy with Kamal, then smoke test live
	bin/deploy
	bin/smoke $(SITE)

backup: ## pg_dump production DB to backups/
	@mkdir -p backups
	$(SSH) 'docker exec inulty-db pg_dump -U appuser -Fc inultycom_prod' \
		> backups/inultycom-$$(date +%Y%m%d-%H%M%S).dump
	@ls -lh backups | tail -1

outdated: ## List direct Python deps with newer versions
	uv tree --outdated --depth 1

upgrade: ## Upgrade Python deps within pyproject.toml ranges (updates uv.lock)
	uv lock --upgrade
	uv sync --locked
