from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "markdownify.apps.MarkdownifyConfig",
    "main.apps.MainConfig",
    "blog.apps.BlogConfig",
    "livereload",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "axes",
]

AUTHENTICATION_BACKENDS = [
    # Must be first: refuses authentication while a lockout is active.
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

MIDDLEWARE = [
    "inultycom.middleware.HealthCheckMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Must be last: renders the lockout response.
    "axes.middleware.AxesMiddleware",
]

# Admin login brute-force protection (django-axes). Lock out an IP after 5 failed
# logins for any username, and a username after 5 failures from any IP, for an
# hour. A successful login clears the count. If you lock yourself out:
#   kamal manage axes_reset_username <username>   (or axes_reset to clear all)
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1  # hours
AXES_LOCKOUT_PARAMETERS = ["ip_address", "username"]
AXES_RESET_ON_SUCCESS = True
AXES_CLIENT_IP_CALLABLE = "inultycom.client_ip.get_client_ip"

ROOT_URLCONF = "inultycom.urls"

# Contact and company details shown on every page (main.context_processors.site).
# UK companies must show their number and registered office on their website.
# A value set to None is hidden. The contact email is stored encoded so it's not in
# this public repo or the HTML as text; main.js decodes it in the browser. To change
# it: python -c "from main.context_processors import encode_email as e; print(e('you@example.com'))"
CONTACT_EMAIL_ENCODED = "bW9jLnl0bHVuaUBuaWFp"
COMPANY_NUMBER = "11426762"
REGISTERED_OFFICE = "199 Field End Road, Eastcote, Pinner, HA5 1QZ, United Kingdom"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "main.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "inultycom.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "assets/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = [ 'main/static/dist']

# WHITENOISE_MIMETYPES = {
#         'bundle.css': 'text/css',
#         'bundle.js': 'application/javascript',
#
#         }
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MARKDOWNIFY = {
    "default": {
        "BLEACH": False,
        "MARKDOWN_EXTENSIONS": ["fenced_code", "codehilite", "attr_list", "tables", ],
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "%(name)-12s %(levelname)-8s %(message)s"},
        "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "file",
            "filename": "/tmp/debug.log",
        },
    },
    "loggers": {"": {"level": "DEBUG", "handlers": ["console", "file"]}},
}
