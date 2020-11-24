

import os
from datetime import datetime, timedelta
from email.utils import parseaddr

from django.utils.translation import ugettext_lazy as _

import environ


env = environ.Env(DEBUG=(bool, False),)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def mkpath(*parts):
    return os.path.abspath(os.path.join(BASE_DIR, *parts))


DEBUG = env.bool('DEBUG', default=False)
SECRET_KEY = env.str('SECRET_KEY', default=('' if not DEBUG else 'xxx'))
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='').split()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ADMINS = [parseaddr(addr) for addr in env('ADMINS', default='').split(',') if addr]

# Sending email
if env('EMAIL_HOST', default=''):
    EMAIL_HOST = env('EMAIL_HOST')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='spam@example.com')

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'atlasso',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'kompassi_oauth2.backends.KompassiOAuth2AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            mkpath('kompassi', 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('pypugjs.ext.django.Loader', (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ))
            ],
            'builtins': [
                'pypugjs.ext.django.templatetags',
            ],
        },
    },
]


ROOT_URLCONF = 'atlasso.urls'

WSGI_APPLICATION = 'atlasso.wsgi.application'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': ':memory:',
  }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        },
        'kompassi_oauth2': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        },
        'atlasso': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': True
        },
    }
}

LANGUAGE_CODE = 'fi-fi'

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = mkpath('static')

KOMPASSI_INSTALLATION_SLUG = env('KOMPASSI_INSTALLATION_SLUG', default='turska')
KOMPASSI_HOST = env('KOMPASSI_HOST', default='https://kompassi.eu')
KOMPASSI_OAUTH2_AUTHORIZATION_URL = '{KOMPASSI_HOST}/oauth2/authorize'.format(**locals())
KOMPASSI_OAUTH2_TOKEN_URL = '{KOMPASSI_HOST}/oauth2/token'.format(**locals())
KOMPASSI_OAUTH2_CLIENT_ID = env('KOMPASSI_OAUTH2_CLIENT_ID', default='kompassi_insecure_test_client_id')
KOMPASSI_OAUTH2_CLIENT_SECRET = env('KOMPASSI_OAUTH2_CLIENT_SECRET', default='kompassi_insecure_test_client_secret')
KOMPASSI_OAUTH2_SCOPE = ['read']
KOMPASSI_API_V2_USER_INFO_URL = '{KOMPASSI_HOST}/api/v2/people/me'.format(**locals())
KOMPASSI_API_V2_EVENT_INFO_URL_TEMPLATE = '{kompassi_host}/api/v2/events/{event_slug}'
KOMPASSI_ADMIN_GROUP = env('KOMPASSI_ADMIN_GROUP', default='admins')
KOMPASSI_ACCESS_GROUP = None

KOMPASSI_CROWD_URL = env('KOMPASSI_CROWD_URL', default='https://crowd.tracon.fi/crowd')
KOMPASSI_CROWD_APPLICATION_NAME = env('KOMPASSI_CROWD_APPLICATION_NAME', default='atlasso')
KOMPASSI_CROWD_APPLICATION_PASSWORD = env('KOMPASSI_CROWD_APPLICATION_PASSWORD', default='secret')
KOMPASSI_CROWD_SESSION_URL = '{KOMPASSI_CROWD_URL}/rest/usermanagement/1/session'.format(**locals())
KOMPASSI_CROWD_VALIDATION_FACTORS = {
    'remote_address': lambda request: '127.0.0.1',
    'X-Forwarded-For': lambda request: request.META['HTTP_X_FORWARDED_FOR'],
}
KOMPASSI_CROWD_COOKIE_ATTRS = dict(
    key='crowd.token_key',
    httponly=True,
    secure=True,
    domain='.tracon.fi',
    path='/',
)

LOGIN_URL = '/oauth2/login'
LOGOUT_URL = '/logout'

ATLASSO_DEFAULT_REDIRECT_URL = env('ATLASSO_DEFAULT_REDIRECT_URL', default='https://confluence.tracon.fi')
ATLASSO_DEFAULT_LOGOUT_REDIRECT_URL = env('ATLASSO_DEFAULT_LOGOUT_REDIRECT_URL', default='https://kompassi.eu/logout')
