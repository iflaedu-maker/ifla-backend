"""
Django settings for ifla_backend project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production-!@#$%^&*()')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS - split by comma, strip whitespace, filter empty strings
# In production, ALLOWED_HOSTS must include your Render domain
allowed_hosts_str = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_str.split(',') if host.strip()]

# For Render health checks, also allow the service hostname if available
if os.getenv('RENDER_EXTERNAL_HOSTNAME'):
    render_host = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    if render_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(render_host)

# Also check for RENDER_SERVICE_HOST (another Render env var)
if os.getenv('RENDER_SERVICE_HOST'):
    render_service_host = os.getenv('RENDER_SERVICE_HOST')
    if render_service_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(render_service_host)

# If DEBUG is False but ALLOWED_HOSTS is empty or only has localhost, add common Render patterns
if not DEBUG and len(ALLOWED_HOSTS) == 1 and 'localhost' in ALLOWED_HOSTS[0]:
    # Allow all .onrender.com domains as fallback
    ALLOWED_HOSTS.append('*.onrender.com')
    # Also allow empty (not recommended but helps debug)
    if not os.getenv('ALLOWED_HOSTS'):
        ALLOWED_HOSTS = ['*']  # Temporary - allows any host


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'accounts',
    'courses',
    'contact',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add WhiteNoise for static files
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ifla_backend.urls'

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

WSGI_APPLICATION = 'ifla_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Use PostgreSQL in production (Render provides DATABASE_URL)
# Use SQLite in development
database_url = os.getenv('DATABASE_URL')

if database_url:
    # Production: PostgreSQL
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(
                default=database_url,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    except ImportError:
        # Fallback if dj_database_url not installed
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    except Exception as e:
        # Log database config error but don't crash
        print(f"Database configuration error: {e}")
        # Fallback to SQLite
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # Development: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
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

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Static files storage for production
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Optional: Use S3 for media in production
USE_S3_MEDIA = os.getenv('USE_S3_MEDIA', 'False').lower() == 'true'
if USE_S3_MEDIA or os.getenv('AWS_STORAGE_BUCKET_NAME'):
    # Ensure storages app is available
    if 'storages' not in INSTALLED_APPS:
        INSTALLED_APPS.append('storages')

    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME', '')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', '')
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    # Optional custom domain (CloudFront or bucket website)
    AWS_S3_CUSTOM_DOMAIN = os.getenv('AWS_S3_CUSTOM_DOMAIN', '')

    # Use S3 for media files only; keep static on WhiteNoise
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    if AWS_S3_CUSTOM_DOMAIN:
        MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    elif AWS_STORAGE_BUCKET_NAME:
        MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"

# WhiteNoise for serving static files in production
if not DEBUG:
    # Use CompressedManifestStaticFilesStorage for better performance
    # This includes videos and all static assets
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # WhiteNoise configuration for better video serving
    WHITENOISE_MAX_AGE = 31536000  # 1 year cache for static files
    WHITENOISE_USE_FINDERS = True  # Help WhiteNoise find static files

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# CORS Configuration
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]
    CORS_ALLOW_ALL_ORIGINS = True  # For development only
else:
    # Production: Only allow your domain
    allowed_origins = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in allowed_origins if origin.strip()]
    CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_CREDENTIALS = True

# CSRF Configuration
if DEBUG:
    CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
else:
    # Production: Use HTTPS
    trusted_origins = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in trusted_origins if origin.strip()]
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = True

# Email Configuration (for contact form and OTP)
# Development: Console backend (prints emails to terminal)
# Production: SMTP backend (sends real emails)

# Determine environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development').lower()

if ENVIRONMENT == 'production':
    # Production: Use SMTP backend
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    
    # Email service configuration (set these via environment variables)
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
    EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() == 'true'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'noreply@ifla.com')
    
    # Optional: Fail silently in production (recommended: False to catch email issues)
    EMAIL_FAIL_SILENTLY = os.getenv('EMAIL_FAIL_SILENTLY', 'False').lower() == 'true'
else:
    # Development: Console backend
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'noreply@ifla.com'

# Google OAuth Configuration
# Get your credentials from: https://console.cloud.google.com/apis/credentials
GOOGLE_OAUTH2_CLIENT_ID = os.getenv('GOOGLE_OAUTH2_CLIENT_ID', '')
GOOGLE_OAUTH2_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET', '')
GOOGLE_OAUTH2_REDIRECT_URI = os.getenv('GOOGLE_OAUTH2_REDIRECT_URI', 'http://localhost:8000/api/auth/google/callback/')

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = False  # Render handles SSL, set to False
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
else:
    # In development, allow all hosts
    if '*' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS = ['*']

# Razorpay Payment Gateway Configuration
# Get your keys from: https://dashboard.razorpay.com/app/keys
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')
# For testing, you can use test keys from Razorpay dashboard
# In production, use environment variables:
# RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
# RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')

