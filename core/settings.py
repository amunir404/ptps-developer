"""
Django settings for bawaslu project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from django.contrib.messages import constants as messages
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#!zp@mi7myd&%!eb4g^w06##@_v^&1#vgrg$p^#+c2l(f(vu7#"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "compressor",
    "accounts",
    "crispy_forms",
    "crispy_tailwind",
    "captcha",
    "django_recaptcha",
    "perolehansuara",
    "wilayah",
    "bawaslu",
    "ptps",
    "import_export",
    "laporanhasil",
    "webpack_loader",
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"


CRISPY_TEMPLATE_PACK = "tailwind"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.get_ptps",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "db_ptps",
        "USER": "amunir404",
        "PASSWORD": "Karawang45",
        "HOST": "ptpsinstance.c9uy2i8cmsm1.ap-southeast-1.rds.amazonaws.com",
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "id"

TIME_ZONE = "Asia/Jakarta"
DATE_INPUT_FORMATS = ["DD-MM-YYYY hh.mm A"]

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = "accounts.User"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

COMPRESS_ENABLED = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = ["core/static"]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # other finders..
    "compressor.finders.CompressorFinder",
)
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "assets"),)

WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "webpack_bundles/",
        "CACHE": not DEBUG,
        "STATS_FILE": os.path.join(BASE_DIR, "webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}

# Media file Configuration
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}
# GOOGLE API
GOOGLE_API_KEY = "AIzaSyDCtjyCBw8wRpDyHxwj9Z3ywQ9IcdilJGA"

RECAPTCHA_PUBLIC_KEY = "6Ldg1x8nAAAAAAnL5BE1KMWjvnHVzOtMJEVbPkXa"
RECAPTCHA_PRIVATE_KEY = "6Ldg1x8nAAAAAH5JVc30cGja-Zif7cv7ld8_LeCx"

CAPTCHA_FONT_SIZE = 30
CAPTCHA_LENGTH = 5
CAPTCHA_IMAGE_SIZE = (150, 50)

LOGIN_REDIRECT_URL = "/"

AWS_ACCESS_KEY_ID = 'AKIAZI2LCEBRHHQCG5I5'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'ptps'
AWS_S3_SIGNATURE_NAME = "s3v3"
AWS_S3_REGION_NAME = 'ap-southeast-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'