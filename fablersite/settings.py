"""
Django settings for fablersite project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bupx2z9jl#x*w$ywj*zxwi!@l2h-c5%h3i-km0)oc9z$dpe9ak'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#AUTH_USER_MODEL = 'main.Listener'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #outside apps
    'oauth2_provider',
    'rest_framework',
    # 'drf_chaos',
    # 'sslserver',

    
    # in-house apps
    # 'splash',
    'authentication',
    'podcast',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'fablersite.urls'

#Registration Settings
#REGISTRATION_OPEN = True                # If True, users can register
#ACCOUNT_ACTIVATION_DAYS = 7     # One-week activation window; you may, of course, use a different value.
#REGISTRATION_AUTO_LOGIN = True  # If True, the user will be automatically logged in.
#LOGIN_REDIRECT_URL = '/accounts/'  # The page you want users to arrive at after they successful log in
#LOGIN_URL = '/accounts/login/'  # The page users are directed to if they are not logged in,
                                                                # and are trying to access pages requiring authentication
#TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

#Security settings
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True
#os.environ['wsgi.url_scheme'] = 'https'

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
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.core.context_processors.request',
  'django.contrib.auth.context_processors.auth',
  'django.template.context_processors.debug',
  'django.template.context_processors.i18n',
  'django.template.context_processors.media',
  'django.template.context_processors.static',
  'django.template.context_processors.tz',
  'django.contrib.messages.context_processors.messages'
)

WSGI_APPLICATION = 'fablersite.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.yahoo.YahooOpenId',
    'django-dual-authentication.backends.DualAuthentication',
    # 'django.contrib.auth.backends.ModelBackend',
)

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

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
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        #'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.permissions.IsAdminUser',
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "www", "static")
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, "static"),
)


#REMOVE THIS AFTER UPDATING DJANGO-REGISTRATION-REDUX TO 1.3
import logging, copy
from django.utils.log import DEFAULT_LOGGING

LOGGING = copy.deepcopy(DEFAULT_LOGGING)
LOGGING['filters']['suppress_deprecated'] = {
    '()': 'fablersite.settings.SuppressDeprecated'  
}
LOGGING['handlers']['console']['filters'].append('suppress_deprecated')

class SuppressDeprecated(logging.Filter):
    def filter(self, record):
        WARNINGS_TO_SUPPRESS = [
            #'RemovedInDjango18Warning',
            'RemovedInDjango19Warning'
        ]
        # Return false to suppress message.
        return not any([warn in record.getMessage() for warn in WARNINGS_TO_SUPPRESS])
