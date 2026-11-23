# inultycom


## Development

### Python environment
Python comes from mise (`.mise.toml`) and dependencies are managed with
[uv](https://docs.astral.sh/uv/): `pyproject.toml` lists them, `uv.lock` pins them.
mise creates `./.venv` with uv and activates it in this directory, so `python` is
always the mise-managed 3.13 venv. The Makefile loads mise's `PATH` itself, so
`make` targets get the same `python` even outside an activated shell.

```
make setup             # mise install + uv sync (+ JS deps, assets, local DB)
uv add <package>       # add a dependency (updates pyproject.toml and uv.lock)
make outdated          # direct deps with newer versions
make upgrade           # upgrade within the ranges in pyproject.toml
```

To rebuild the venv: `rm -rf .venv && make setup`.

Settings are picked with `DJANGO_SETTINGS_MODULE=inultycom.environments.{dev,prod}`.

### Run dev server
```
make setup      # once: venv, Python + JS deps, assets, local DB
make dev        # http://localhost:8000 with livereload and the asset watcher
make superuser  # local admin user, to preview drafts at /blog/<slug>
```

Local dev uses SQLite (`db.sqlite3`, gitignored), so no database server is needed.
Set `DATABASE_URL` in `.env.dev` to use Postgres instead.

Preview a Markdown post without the database at
`http://localhost:8000/blog/preview/<file>.md`; it reloads when the file is saved.

### Using yarn 2/3

Disable global yarn in mise with .mise.toml

<--! https://nodejs.org/api/corepack.html -->
```
corepack enable
corepack use yarn@3.8.7
```

# Saving installed package

pip 

## Build
key files

inultycom main config
main is the main app 
blog is the blog
admin is the admin

|What is it|path|Description|
|---|---|---|
|Routing| inultycom/urls.py| Defines all the routes from all the sub apps (main/blog/admin)|
|Src Assets| main/static/src| This is the directory where assets are changed|
|Prod Assets| assets| Assets copied from dist|
|Routing| inultycom/urls.py||
|Routing| inultycom/urls.py||

### Assets


Assets source lives in main/

## Deployment

Deployed to a DigitalOcean droplet with [Kamal](https://kamal-deploy.org) (`config/deploy.yml`).
Kamal is pinned in `.mise.toml`, so `mise install` provides it.

- **App**: built from `Dockerfile`, pushed to `registry.digitalocean.com/inultycom/inultycom`,
  served by gunicorn behind `kamal-proxy` (TLS via Let's Encrypt for inulty.com and www.inulty.com).
  Static files are served by WhiteNoise under `/assets/`.
- **DB**: Postgres accessory `inulty-db`, reachable only on the private `kamal` Docker network.
  Data lives on the block volume at `/mnt/inultycom_vol1/postgres/data`.
- **Health check**: `/up`, answered by `inultycom.middleware.HealthCheckMiddleware`.
- **Secrets**: `.kamal/secrets` (gitignored; never commit it). Needs `SECRET_KEY`,
  `POSTGRES_PASSWORD` and `DATABASE_URL`; the registry token comes from `$KAMAL_REGISTRY_PASSWORD`.

Local tasks are in the `Makefile` (`make` lists them); server tasks are Kamal aliases.

```
export KAMAL_REGISTRY_PASSWORD=<DigitalOcean API token>
make smoke            # build the image, test it against a throwaway Postgres
make deploy           # check + smoke, kamal deploy, then smoke test the live site
make smoke-live       # smoke test https://inulty.com
make backup           # pg_dump production to backups/

kamal logs            # tail app logs
kamal shell           # shell in the app container
kamal manage <cmd>    # e.g. kamal manage createsuperuser
kamal dbc             # psql in the db container
```
