import environ
from .settings import *

# All config is injected as environment variables by Kamal (see config/deploy.yml
# and .kamal/secrets). Nothing is read from files baked into the image.
env = environ.Env()

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

# kamal-proxy terminates TLS and sets X-Forwarded-Proto
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DATABASES = {
    "default": env.db()
}

# Containers log to stdout (`kamal logs`); no log file inside the image.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"console": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "console"}},
    "root": {"level": env("LOG_LEVEL", default="INFO"), "handlers": ["console"]},
}
