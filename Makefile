# Local tasks. Server-side tasks are Kamal aliases (config/deploy.yml):
#   kamal logs | shell | manage <cmd> | dbc | dblogs

SITE      := https://inulty.com
SERVER    := root@178.128.165.170
SSH_KEY   := ~/.ssh/inulty_digitalocean_ed25519
SSH       := ssh -i $(SSH_KEY) -o IdentitiesOnly=yes $(SERVER)
PY        := venv/bin/python
# Enough env for prod settings to load without a real database
CHECK_ENV := DJANGO_SETTINGS_MODULE=inultycom.environments.prod SECRET_KEY=check-only-not-a-real-key-0123456789abcdefghijklmnopqrstuvwxyz \
             DATABASE_URL=sqlite://:memory: ALLOWED_HOSTS=inulty.com

.DEFAULT_GOAL := help
.PHONY: help setup dev assets check image smoke smoke-live deploy backup outdated

help: ## List tasks
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  \033[36m%-11s\033[0m %s\n", $$1, $$2}'

setup: ## Create venv, install Python and JS deps
	test -d venv || python -m venv venv
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt
	yarn install

dev: ## Run dev server, livereload and asset watcher (foreman)
	bin/foreman

assets: ## Build the JS/CSS bundle
	yarn build

check: ## Django system checks + missing migrations, against prod settings
	$(CHECK_ENV) $(PY) -Wd manage.py check --deploy --fail-level ERROR
	$(CHECK_ENV) $(PY) manage.py makemigrations --check --dry-run

image: ## Build the production Docker image
	docker build --platform linux/amd64 -t inultycom .

smoke: ## Build the image and smoke test it against a throwaway Postgres
	bin/smoke

smoke-live: ## Smoke test the live site
	bin/smoke $(SITE)

deploy: check smoke ## Check, smoke test, deploy with Kamal, then smoke test live
	bin/deploy
	bin/smoke $(SITE)

backup: ## pg_dump production DB to backups/
	@mkdir -p backups
	$(SSH) 'docker exec inulty-db pg_dump -U appuser -Fc inultycom_prod' \
		> backups/inultycom-$$(date +%Y%m%d-%H%M%S).dump
	@ls -lh backups | tail -1

outdated: ## List outdated Python packages
	$(PY) -m pip list --outdated
