"""
These test settings override the main settings for testing purposes.
"""

from core.settings import *

# Use in-memory SQLite database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable caching during tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Use faster password hasher during tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable debugging
DEBUG = False

# Disable logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'root': {
        'handlers': ['null'],
        'level': 'CRITICAL',
    },
}

# Use test email backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable CSRF validation in tests
MIDDLEWARE = [
    middleware for middleware in MIDDLEWARE
    if middleware != 'django.middleware.csrf.CsrfViewMiddleware'
]

# Test-specific apps
INSTALLED_APPS += [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
]

# REST Framework test settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': None,
    'PAGE_SIZE': None,
}

# Media files configuration for tests
MEDIA_ROOT = tempfile.mkdtemp()

# Static files configuration for tests
STATIC_ROOT = tempfile.mkdtemp()

# Security settings for tests
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'test-key-not-for-production'

# Disable password validation during tests
AUTH_PASSWORD_VALIDATORS = []

# Test-specific constants
TEST_PHONE_NUMBER = '+11234567890'
TEST_PASSWORD = 'testpass123'
TEST_USERNAME = 'testuser'

# Rate limiting settings for tests
RATELIMIT_ENABLE = False

# JWT settings for tests
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Add required imports at the top
import tempfile
from datetime import timedelta