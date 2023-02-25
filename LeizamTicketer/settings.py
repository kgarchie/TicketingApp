"""
Django settings for LeizamTicketer project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import logging
import os.path
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # SECURITY WARNING: don't run with debug turned on in production!
    # Default value is True, but it will be overriden by the .env file
    DEBUG=(bool, True)
)

# if there is a file named .env.prod in the base directory, use it
if os.path.exists(BASE_DIR / '.env.prod'):
    if os.path.exists(BASE_DIR / '.env.dev'):
        environ.Env.read_env(env_file='.env.dev')
        logging.info('Using .env.dev environment file')
    else:
        environ.Env.read_env(env_file='.env.prod')
        logging.warning('Using .env.prod file')

elif os.path.exists(BASE_DIR / '.env'):
    environ.Env.read_env(env_file='.env')
    logging.info('Using Fallback .env')

else:
    raise FileNotFoundError('No .env file found the file is required for the project to run')

# Set new DEBUG value after reading the .env file
DEBUG = env('DEBUG')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# This doesn't work as intended. It doesn't return a proper list.
# Instead, it returns a string even when I try to convert it to a list
ALLOWED_HOSTS = list(str(env.get_value("ALLOWED_HOSTS")).split(',')) if len(env('ALLOWED_HOSTS')) > 0 else ['*']

# if environment is production
if not DEBUG:
    if len(ALLOWED_HOSTS) == 0:
        raise ValueError('No allowed hosts found in the .env file')

# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'TicketingApp.apps.TicketingAppConfig',
    'chat.apps.ChatConfig',
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

ROOT_URLCONF = 'LeizamTicketer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'LeizamTicketer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# if debug is true use sqlite3, else use mysql
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': env('DATABASE_ENGINE'),
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'HOST': env('DATABASE_HOST'),
            'PORT': env('DATABASE_PORT')
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ASGI_APPLICATION = "LeizamTicketer.asgi.application"

AUTHENTICATION_BACKENDS = ['TicketingApp.auth.custom_auth']

SESSION_ENGINE = 'django.contrib.sessions.backends.file'

SESSION_FILE_PATH = BASE_DIR / 'sessions'
