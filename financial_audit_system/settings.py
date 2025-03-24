"""
Django settings for financial_audit_system project.

Generated by 'django-admin startproject' using Django 4.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import dj_database_url
import os

import environ

env = environ.Env()
environ.Env.read_env()  # Reads from .env file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-5^&0e_c%w2pg2x=b5&)v0glw=u55a9v+wqg8p95++p6wpm2y@d'
SECRET_KEY = [os.getenv("SECRET_KEY")]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("ENV") != "production"

# ALLOWED_HOSTS = ["financial-audit-system.herokuapp.com"]
# ALLOWED_HOSTS = [os.getenv("RAILWAY_DOMAIN", "127.0.0.1")]
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1").split(",")

CSRF_TRUSTED_ORIGINS = [f"https://{os.getenv('RAILWAY_DOMAIN')}"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'audit',
    'rest_framework',
    'bootstrap4',
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

ROOT_URLCONF = 'financial_audit_system.urls'

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

WSGI_APPLICATION = 'financial_audit_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
        
#         # 'USER': 'root',
#         # 'PASSWORD': 'root',
#         # 'HOST': 'localhost',
#         # 'PORT': '3306'
#     }
# }

if os.getenv("ENV") == "production":
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
        }
    
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'financial_audit_db',
            'USER': 'postgres',
            'PASSWORD': os.getenv('DB_PASSWORD', 'yourpassword'),
            'HOST': 'localhost',
            'PORT': '5432',
            # 'NAME': BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

# Whitenoise settings
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
