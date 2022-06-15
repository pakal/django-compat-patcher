"""
Django settings for test_project project.

Generated by 'django-admin startproject' using Django 1.9.6.
"""

import django

django_version = django.VERSION

from .minimal_settings import *


SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "test_project",

    # To access their middlewares for patching:
    "django.contrib.redirects",
    "django.contrib.flatpages",
]

SILENCED_SYSTEM_CHECKS = [
    "fields.E903",  # NullBooleanField is removed except for support in historical migrations
    "fields.E904",  # django.contrib.postgres.fields.JSONField is removed except for support in historical migrations
]

if not os.environ.get("IGNORE_CONTRIB_COMMENTS"):
    # old contrib packages, restored by proxifier in their original django.contrib.* namespace
    INSTALLED_APPS.append(
        "django_comments" if django_version >= (1, 8) else "django.contrib.comments"
    )


MIDDLEWARE_CLASSES = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
MIDDLEWARE = MIDDLEWARE_CLASSES


ROOT_URLCONF = "test_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "allowed_include_roots": [BASE_DIR],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

WSGI_APPLICATION = "test_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "test_project", "db.sqlite3"),
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = "/static/"

