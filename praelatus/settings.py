"""
Django settings for praelatus project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from .celery import app as celery_app

__all__ = ['celery_app']

RELEASE_NAME = 'Rio Bravo'
VERSION = '0.1.0'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.getenv('PRAELATUS_DATA_DIR', os.path.join(BASE_DIR, 'data'))

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

APPEND_SLASH = False

SECRET_KEY = ''
# SECURITY WARNING: keep the secret key used in production secret!
if os.path.exists(os.path.join(DATA_DIR, '.secret_key')):
    with open(os.path.join(DATA_DIR, '.secret_key')) as f:
        SECRET_KEY = f.read()
else:
    with open(os.path.join(DATA_DIR, '.secret_key'), 'w') as f:
        import binascii
        rand = os.urandom(24)
        SECRET_KEY = binascii.b2a_hex(rand).decode('ascii')
        f.write(SECRET_KEY)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('PRAELATUS_DEBUG', 'False'))

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # Row level security
    'guardian',
    # Filtering of models
    'django_filters',
    # REST API
    'rest_framework',

    # Praelatus
    'projects.apps.ProjectsConfig',
    'workflows.apps.WorkflowsConfig',
    'tickets.apps.TicketsConfig',
    'labels.apps.LabelsConfig',
    'fields.apps.FieldsConfig',
    'profiles.apps.ProfilesConfig',
    'hooks.apps.HooksConfig',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

ROOT_URLCONF = 'praelatus.urls'


def version_number(request):
    return {'version_number': VERSION}


def release_name(request):
    return {'release_name': RELEASE_NAME}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'praelatus.settings.version_number',
                'praelatus.settings.release_name',
            ],
        },
    }
]

WSGI_APPLICATION = 'praelatus.wsgi.application'


# DATABASE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PRAELATUS_DB_NAME', 'praelatus'),
        'USER': os.getenv('PRAELATUS_DB_USER', 'postgres'),
        'PASSWORD': os.getenv('PRAELATUS_DB_PASS', 'postgres'),
        'HOST': os.getenv('PRAELATUS_DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('PRAELATUS_DB_PORT', '5432')
    },
}

if os.getenv('PRAELATUS_USE_SQLITE'):
    print('Using SQLITE database, this is not recommended for production!')
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': './db.sqlite3',
    }


# AUTHENTICATION

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
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

AUTH_PROFILE_MODULE = 'profiles.Profile'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(DATA_DIR, 'static')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


# CACHING

CACHES = {
    "default": {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('PRAELATUS_REDIS', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': 'example'
    }
}

# CELERY

CELERY_BROKER_URL = os.getenv('PRAELATUS_MQ_SERVER', CACHES['default']['LOCATION'])
CELERY_RESULT_BACKEND = 'rpc://'

# REST

REST_FRAMEWORK = {
    # Integrate Django Filters
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    # Use sessions or basic auth
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
