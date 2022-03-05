"""
Django settings for ctudy_server project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import json
import os
from pathlib import Path

ENV = os.environ.get('DB_PORT', 'DEV')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m&=f82t@_w+w0z2(8(lc1=3)om6^3=8f3kf_qqljto@acbp=ra'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'account',
    'coupon',
    'room'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'ctudy_server.urls'

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

WSGI_APPLICATION = 'ctudy_server.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
ACCESS_CONTROL_EXPOSE_HEADERS = ['Content-Disposition']

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'ctudy_server.pagination.CustomPagination',
    'PAGE_SIZE': 10
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if ENV == 'DEV':
    # secret file
    with open('./ctudy_server/secret.json', 'r', encoding='utf-8') as f:
        secret = json.load(f)

    DATABASES = {
        # 'default': {
        #    'ENGINE': 'django.db.backends.sqlite3',
        #    'NAME': BASE_DIR / 'db.sqlite3',
        # }
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': secret['DB']['NAME'],
            'HOST': secret['DB']['HOST'],
            'PORT': secret['DB']['PORT'],
            'USER': secret['DB']['USER'],
            'PASSWORD': secret['DB']['PASSWORD'],
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['DB_NAME'],
            'HOST': os.environ['DB_HOST'],
            'PORT': os.environ['DB_PORT'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASSWORD'],
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging Setting
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'format1': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 10,
            'filename': os.path.join(BASE_DIR, 'logs/backend_api.log'),
            'formatter': 'format1',
        }
    },
    'loggers': {
        'account': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        'room': {
            'handlers': ['file'],
            'level': 'DEBUG'
        },
        'coupon': {
            'handlers': ['file'],
            'level': 'DEBUG'
        }
    }
}

TOKEN_URL = 'http://localhost:8000/o/token/'
APP_NAME = 'ctudy'