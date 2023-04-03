import environ
import os
from .settings import *

# set casting, default value
DEBUG=True
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
env_file = os.path.join(BASE_DIR, ".env")

env.read_env(env_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": env.db()
}
