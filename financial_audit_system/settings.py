"""
Django settings for financial_audit_system project.
Optimized for Railway deployment
"""

from pathlib import Path
import dj_database_url
import os
import environ
import socket

# Initialize environment
env = environ.Env()
environ.Env.read_env()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.getenv("SECRET_KEY", env('SECRET_KEY', default='your-default-secret-key'))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Railway detection
IS_RAILWAY = 'RAILWAY_ENVIRONMENT' in os.environ
IS_PRODUCTION = os.getenv('ENV') == 'production' or IS_RAILWAY

ALLOWED_HOSTS = ['python-financialaudit.onrender.com', 'localhost', '127.0.0.1']

# Add wildcard for development
if DEBUG:
    ALLOWED_HOSTS.append('*')

CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    "https://python-financialaudit-production.up.railway.app",
    "https://python-financialaudit.onrender.com"
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',  # Add this
    'audit',
    'rest_framework',
    'bootstrap4',
]

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

ROOT_URLCONF = 'financial_audit_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Configure the default database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600,
        ssl_require=IS_PRODUCTION
    )
}

# Apply PostgreSQL-specific optimizations only if using PostgreSQL
default_db_engine = DATABASES['default'].get('ENGINE', '')
if 'postgresql' in default_db_engine or 'psycopg2' in default_db_engine:
    DATABASES['default']['OPTIONS'] = {
        'connect_timeout': 10,
        'keepalives': 1,
        'keepalives_idle': 30,
        'keepalives_interval': 10,
        'keepalives_count': 5,
    }

    if IS_PRODUCTION:
        DATABASES['default']['OPTIONS']['sslmode'] = 'require'

        
# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (Whitenoise)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security headers
if IS_PRODUCTION:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
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

# Health check settings
HEALTHCHECK_ENABLED = os.getenv('HEALTHCHECK_ENABLED', 'true').lower() == 'true'

# Railway-specific settings
if IS_RAILWAY:
    PORT = os.getenv('PORT', '8000')
    # Ensure debug is off in production
    if IS_PRODUCTION:
        DEBUG = False
    # Additional production optimizations
    DATABASES['default']['CONN_MAX_AGE'] = 60

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'