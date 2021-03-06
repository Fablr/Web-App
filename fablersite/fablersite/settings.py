import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bupx2z9jl#x*w$ywj*zxwi!@l2h-c5%h3i-km0)oc9z$dpe9ak'

# SECURITY WARNING: don't run with debug turned on in production!
FACEBOOK_SOCIAL_AUTH_RAISE_EXCEPTIONS = True
SOCIAL_AUTH_RAISE_EXCEPTIONS = True
RAISE_EXCEPTIONS = True
DEBUG = True

ALLOWED_HOSTS = ['localhost:8000']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'oauth2_provider',
    'rest_framework',
    'django_hosts',
    'corsheaders',
    'threaded_comments',
    'authentication',
    'podcast',
    'feed',
)

MIDDLEWARE_CLASSES = (
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
)

ROOT_URLCONF = 'fablersite.urls'
ROOT_HOSTCONF = 'fablersite.hosts'
DEFAULT_HOST = 'www'

if 'RDS_DB_NAME' in os.environ:
    SESSION_COOKIE_DOMAIN = '.fablersite-dev.elasticbeanstalk.com'
    CORS_ORIGIN_WHITELIST = (
        'fablersite-dev.elasticbeanstalk.com',
        'ec2-54-218-65-165.us-west-2.compute.amazonaws.com',
    )
else:
    SESSION_COOKIE_DOMAIN = '.test.com'
    CORS_ORIGIN_WHITELIST = (
        'test.com:8000',
        'test.com:5555',
        'test.com:8080',
        'ec2-54-218-65-165.us-west-2.compute.amazonaws.com',
    )

CORS_ALLOW_CREDENTIALS = True

CSRF_COOKIE_SECURE = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fablersite.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django-dual-authentication.backends.DualAuthentication',
)

SOCIAL_AUTH_FACEBOOK_KEY = os.environ['FB_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['FB_SECRET']
LOGIN_REDIRECT_URL = '/'

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'local_django_fabler',
            'USER': os.environ['USER'],
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        },
        'aws': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'ebdb',
            'USER': 'dreplogle',
            'PASSWORD': os.environ['AWSPASSWORD'],
            'HOST': 'aa1rr2xlfemsxmo.cp4q3xdsxtdz.us-west-2.rds.amazonaws.com',
            'PORT': '5432',
        }
    }

REST_FRAMEWORK = {
    'PAGINATE_BY': 20,
    'MAX_PAGINATE_BY': 20,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.DjangoFilterBackend',
    ],
}

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True

if 'RDS_DB_NAME' in os.environ:
    STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
    STATIC_URL = '/static/'
else:
    STATIC_URL = '/static/'


#REMOVE THIS AFTER UPDATING DJANGO-REGISTRATION-REDUX TO 1.3
import logging
import copy
from django.utils.log import DEFAULT_LOGGING

LOGGING = copy.deepcopy(DEFAULT_LOGGING)
LOGGING['filters']['suppress_deprecated'] = {
    '()': 'fablersite.settings.SuppressDeprecated'
}
LOGGING['handlers']['console']['filters'].append('suppress_deprecated')

if 'RDS_DB_NAME' in os.environ:
    DEBUG_LOG_DIR = '/var/log/app/django_debug.log'
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
        },
        'handlers': {
            'null': {
                'level':'DEBUG',
                'class':'logging.NullHandler',
            },
            'log_file': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': DEBUG_LOG_DIR,
                'maxBytes': 50000,
                'backupCount': 2,
                'formatter': 'standard',
            },
            'console':{
                'level':'INFO',
                'class':'logging.StreamHandler',
                'formatter': 'standard'
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
            },
        },
        'loggers': {
            'repackager': {
                'handlers': ['console', 'log_file'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django': {
                'handlers':['console'],
                'propagate': True,
                'level':'WARN',
            },
            'django.db.backends': {
                'handlers': ['console', 'log_file'],
                'level': 'WARN',
                'propagate': False,
            },
            '': {
                'handlers': ['console', 'log_file'],
                'level': 'DEBUG',
            },
        }
    }

class SuppressDeprecated(logging.Filter):
    def filter(self, record):
        WARNINGS_TO_SUPPRESS = []

        return not any([warn in record.getMessage() for warn in WARNINGS_TO_SUPPRESS])
