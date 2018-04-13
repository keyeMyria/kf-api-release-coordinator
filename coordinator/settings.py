"""
Django settings for coordinator project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import uuid

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(uuid.uuid4())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
APPEND_SLASH = False


# Application definition

INSTALLED_APPS = [
    'coordinator.api.apps.ApiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_rq',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'coordinator.urls'

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

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

WSGI_APPLICATION = 'coordinator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

def get_databases():
    """ Will try to load from vault or default to environmet """
    db = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('PG_NAME', 'dev'),
            'USER': os.environ.get('PG_USER','postgres'),
            'PASSWORD': os.environ.get('PG_PASS', None),
            'HOST': os.environ.get('PG_HOST', '127.0.0.1'),
            'PORT': os.environ.get('PG_PORT', '5432'),
        }
    }
    vault_url = os.environ.get('VAULT_URL', None)
    vault_role = os.environ.get('VAULT_ROLE', None)
    pg_secret = os.environ.get('PG_SECRET', None)
    # Default to the above config if the required vault vars are not present
    if not vault_url or not vault_role or not pg_secret:
        return db

    import hvac
    client = hvac.Client(url=vault_url)
    client.auth_iam(vault_role)
    pg_secrets = client.read(pg_secret)
    client.logout()

    db['default']['USER'] = pg_secrets['data']['user']
    db['default']['PASSWORD'] = pg_secrets['data']['password']

    return db

DATABASES = get_databases()


# Redis
def get_queues():
    """ Will try to load from vault or default to environmet """
    rq = {
        'default': {
            'HOST': os.environ.get('REDIS_HOST', 'localhost'),
            'PORT': os.environ.get('REDIS_PORT', 6379),
            'DB': 0,
            'DEFAULT_TIMEOUT': 360,
        },
    }
    vault_url = os.environ.get('VAULT_URL', None)
    vault_role = os.environ.get('VAULT_ROLE', None)
    redis_secret = os.environ.get('REDIS_SECRET', None)
    # Default to the above config if the required vault vars are not present
    if not vault_url or not vault_role or not redis_secret:
        return rq

    import hvac
    client = hvac.Client(url=vault_url)
    client.auth_iam(vault_role)
    redis_secrets = client.read(redis_secret)
    client.logout()

    rq['default']['PASSWORD'] = redis_secrets['data']['password']

    return rq


RQ_QUEUES = get_queues()

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
