from __future__ import absolute_import
import os
import dj_database_url
from path import path

PROJECT_ROOT = path(__file__).abspath().dirname().dirname().dirname()
os.sys.path.append(PROJECT_ROOT)
os.sys.path.append(PROJECT_ROOT / "app")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ORIGIN_REGEX_WHITELIST = (
    "^(https?://)localhost:\d{4,5}$",
    "^(https?://)localdocker:\d{4,5}$",
)

CORS_ALLOW_HEADERS = (
    "x-requested-with",
    "x-authorization",
    "content-type",
    "accept",
    "origin",
    "authorization",
    "x-csrftoken",
    "x-forwarded-proto",
    "x-forwarded-for",
    "x-forwarded-port",
)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "localdocker",
    "172.17.0.1",
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'api_client',
    'match',
    'summoner',
    'champion'
)

MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = 'app.config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASE_URL = os.environ.get("DATABASE_URL")

DATABASES = {}
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/s
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


LEAGUE_API_KEY = os.environ.get("LEAGUE_API_KEY")
