"""
Django settings for financial_audit_system project.
Optimized for deployment on Railway and Render.
"""

from pathlib import Path
import os
import environ
import dj_database_url

# Initialize environment
env = environ.Env()
environ.Env.read_env()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret Key & Debug
SECRET_KEY = env('SECRET_KEY', default='your-default-secret-key')
DEBUG = env.bool('DEBUG', default=False)

# Deployment Environment
IS_RAILWAY = 'RAILWAY_ENVIRONMENT' in os.environ
IS_PRODUCTION = env('ENV', default='development') == 'production' or IS_RAILWAY

# Allowed Hosts
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[
    'python-financialaudit.onrender.com',
    'localhost',
    '127.0.0.1',
])

if DEBUG:
    ALLOWED_HOSTS += ['*']

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    "https://python-financialaudit-production.up.railway.app",
    "https://python-financialaudit.onrender.com",
]

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'whitenoise.runserver_nostatic',
    'rest_framework',
    'bootstrap4',

    # Local
    'audit',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs & WSGI
ROOT_URLCONF = 'financial_audit_system.urls'
WSGI_APPLICATION = 'financial_audit_system.wsgi.application'

# Templates
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

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=IS_PRODUCTION
    )
}

# PostgreSQL-specific options
db_engine = DATABASES['default'].get('ENGINE', '')
if 'postgresql' in db_engine or 'psycopg2' in db_engine:
    DATABASES['default']['OPTIONS'] = {
        'connect_timeout': 10,
        'keepalives': 1,
        'keepalives_idle': 30,
        'keepalives_interval': 10,
        'keepalives_count': 5,
    }
    if IS_PRODUCTION:
        DATABASES['default']['OPTIONS']['sslmode'] = 'require'

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security Settings for Production
if IS_PRODUCTION:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Health Check Toggle
HEALTHCHECK_ENABLED = env.bool('HEALTHCHECK_ENABLED', default=True)

# Railway Port Setting
if IS_RAILWAY:
    os.environ.setdefault('PORT', '8000')
    if IS_PRODUCTION:
        DEBUG = False
    DATABASES['default']['CONN_MAX_AGE'] = 60

# Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
