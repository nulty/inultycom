# inultycom


## Development

```
source venv/bin/activate
which python # should be venv version
```

### Run dev server
```
DJANGO_SETTINGS_MODULE=inultycom.environments.dev python manage.py runserver
```

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

```
export KAMAL_REGISTRY_PASSWORD=<DigitalOcean API token>
bin/deploy            # kamal deploy
kamal logs            # tail app logs
kamal shell           # shell in the app container
kamal dbc             # psql in the db container
kamal app exec "python manage.py createsuperuser" --interactive
```
