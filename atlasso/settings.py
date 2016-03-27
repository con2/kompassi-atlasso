import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def mkpath(*parts):
    return os.path.abspath(os.path.join(BASE_DIR, *parts))

SECRET_KEY = r'y6LA_G4TmWXwnueq4wdAam=XseKXV=3X3HHJbQRcj1K'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

if DEBUG:
    # XXX Monkey patch is_secure_transport to allow development over insecure HTTP

    from warnings import warn
    warn(UserWarning("Monkey_patching oauthlib.oauth2:is_secure_transport to allow OAuth2 over HTTP. Never do this in production!"))

    fake_is_secure_transport = lambda token_url: True

    import oauthlib.oauth2
    import requests_oauthlib.oauth2_session
    import oauthlib.oauth2.rfc6749.parameters
    import oauthlib.oauth2.rfc6749.clients.base

    for module in [
        oauthlib.oauth2,
        requests_oauthlib.oauth2_session,
        oauthlib.oauth2.rfc6749.parameters,
        oauthlib.oauth2.rfc6749.clients.base,
    ]:
        module.is_secure_transport = fake_is_secure_transport

ALLOWED_HOSTS = ['.tracon.fi']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'atlasso',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'kompassi_oauth2.backends.KompassiOAuth2AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader',(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

ROOT_URLCONF = 'atlasso.urls'

WSGI_APPLICATION = 'atlasso.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'atlasso.sqlite3'),
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
        'console':{
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
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

KOMPASSI_INSTALLATION_SLUG = 'turskadev'
KOMPASSI_HOST = 'http://kompassi.dev:8000'
KOMPASSI_OAUTH2_AUTHORIZATION_URL = '{KOMPASSI_HOST}/oauth2/authorize'.format(**locals())
KOMPASSI_OAUTH2_TOKEN_URL = '{KOMPASSI_HOST}/oauth2/token'.format(**locals())
KOMPASSI_OAUTH2_CLIENT_ID = 'kompassi_insecure_test_client_id'
KOMPASSI_OAUTH2_CLIENT_SECRET = 'kompassi_insecure_test_client_secret'
KOMPASSI_OAUTH2_SCOPE = ['read']
KOMPASSI_API_V2_USER_INFO_URL = '{KOMPASSI_HOST}/api/v2/people/me'.format(**locals())
KOMPASSI_API_V2_EVENT_INFO_URL_TEMPLATE = '{kompassi_host}/api/v2/events/{event_slug}'
KOMPASSI_ADMIN_GROUP = 'admins'
KOMPASSI_ACCESS_GROUP = None

KOMPASSI_CROWD_URL = 'https://crowd.tracon.fi/crowd'
KOMPASSI_CROWD_APPLICATION_NAME = 'atlasso'
KOMPASSI_CROWD_APPLICATION_PASSWORD = 'secret'
KOMPASSI_CROWD_SESSION_URL = '{KOMPASSI_CROWD_URL}/rest/usermanagement/1/session'.format(**locals())
KOMPASSI_CROWD_VALIDATION_FACTORS = {
    'remote_address': lambda request: '127.0.0.1',
    'X-Forwarded-For': lambda request: request.META['REMOTE_ADDR'],
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

ATLASSO_DEFAULT_REDIRECT_URL = 'https://confluence.tracon.fi'
ATLASSO_DEFAULT_LOGOUT_REDIRECT_URL = 'https://kompassi.eu/logout'
