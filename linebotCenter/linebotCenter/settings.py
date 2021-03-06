"""
Django settings for linebotCenter project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import django_heroku
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENTER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"\\gamingcenter"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v7o$*g)_n^_kg)9fpxaygs3clc8h$9o+w*ko!mogq=c#t)g!io'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*'
]

# LINE_CHANNEL_ACCESS_TOKEN = '0CGVjzllPKIDsZwGhWm2znjw0JnL6ep9DzhPTu0ve4F2XpXBGCn6mn1E4HrUG1o8lK8+wJRQ5EnHhGJYcxrmMMp0sVbAMf51CvnhRajD0jOZkW0rd3hP/8rewl8MVkgv2Qa8SyXV/Vox2VSgEyA87AdB04t89/1O/w1cDnyilFU='
# LINE_CHANNEL_SECRET = '4b7dc7c14cdf73785bc3a9f56af7b230'
# Application definition
GROUP_CHANNEL = {
    'LINE_CHANNEL_ACCESS_TOKEN': 'US76JZGHeO85JBm6auzdpPKLHp6BY3XZlBjNbXqL9a4iutAczeYqi3DN/q9CVHIjQgG+scCs5UwsX0Ma/59mwCtP9vAeGFLcimPhJGIHac5uNMP+ZIRkBptNx3LuVJZhA4/x3rKrUP0LuHJTanDHaQdB04t89/1O/w1cDnyilFU=',
    'LINE_CHANNEL_SECRET': 'cbc68547035ab846b8d27534c55d0cec'
}
USER_CHANNEL = {
    'LINE_CHANNEL_ACCESS_TOKEN': 'Ru7/VEWhnvf2LXlYtp7fkYvf6jGj2atEagiLvFVZwUMdOz49DDnEovuAjQDOg1D5TOj2IEtm4kL+q7t8TbK05dKyaVRvO01OBBMOp4kZ9W+Ya5nxUq3uKMc7vKnixA9qJq9n+U+qWNOMBuloOYHn5AdB04t89/1O/w1cDnyilFU=',
    'LINE_CHANNEL_SECRET': '7fe9f31729efd76c3566230047a2b055'
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'gamingcenter.apps.GamingcenterConfig',
    'gaminguser.apps.GaminguserConfig',
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

ROOT_URLCONF = 'linebotCenter.urls'

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

WSGI_APPLICATION = 'linebotCenter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
django_heroku.settings(locals())