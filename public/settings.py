import os
import dj_database_url

oeg = lambda x, y: os.environ.get(x, y)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = os.environ.get('SECRET_KEY', '')


DEBUG = os.environ.get('DJANGO_DEBUG', False)
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = [
    "api.pault.ag",
    "api.lucifer.pault.ag",
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'restless',
    'recdep',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'public.urls'

WSGI_APPLICATION = 'public.wsgi.application'


DATABASES = {
    'default': dj_database_url.parse(os.environ.get(
        'DATABASE_URL',
        'postgis://recdep:recdep@localhost/recdep'
    ))
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

TWILIO_ACCOUNT_SID = oeg("TWILIO_ACCOUNT_SID", None)
TWILIO_AUTH_TOKEN = oeg("TWILIO_AUTH_TOKEN", None)
TWILIO_TO_NUMBER = oeg("TWILIO_TO_NUMBER", "5555555555")
TWILIO_FROM_NUMBER = oeg("TWILIO_FROM_NUMBER", "5555555555")

try:
    from local_settings import *
except ImportError:
    pass
