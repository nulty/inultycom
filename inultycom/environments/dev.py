import environ
import os
from .settings import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Optional overrides in .env.dev. Real environment variables win over the file.
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env.dev"))

SECRET_KEY = env("SECRET_KEY", default="dev-only-insecure-key")

# SQLite by default so local dev needs no database server. Set DATABASE_URL
# (e.g. in .env.dev) to use Postgres instead.
DATABASES = {
    "default": env.db(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}
