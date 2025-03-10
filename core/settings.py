"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from shutil import which
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
import boto3
from botocore.config import Config
# from core.jazzmin_settings import JAZZMIN_SETTINGS

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# settings.py


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
COMPANY_NAME = os.environ.get('COMPANY_NAME')
POSTGRES_NAME = os.environ.get('POSTGRES_NAME')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_PORT = os.environ.get('POSTGREs_PORT')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
DATABASE_URL = os.environ.get('DATABASE_URL')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'

SMTP_PROVIDER = os.environ.get('SMTP_PROVIDER')
SMTP_PORT = os.environ.get('SMTP_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# Replace with your actual key or load from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# Replace with your actual secret or load from environment variables
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# Replace with your S3 bucket name
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
# Replace with your region (e.g., "us-west-1")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# Use Signature Version 4
S3_CLIENT = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME,
    config=Config(signature_version='s3v4')
)

ALLOWED_HOSTS = ['unionwealthbank.com', 'www.unionwealthbank.com',
                 '127.0.0.1', 'guarded-beyond-00794-524fc926f7f4.herokuapp.com',]

CSRF_TRUSTED_ORIGINS = [
    'https://unionwealthbank.com',
    'https://www.unionwealthbank.com',
    'https://guarded-beyond-00794-524fc926f7f4.herokuapp.com',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    "allauth.mfa",
    "allauth.headless",
    "allauth.usersessions",
    "django_countries",
    "phonenumber_field",
    'django_filters',
    'widget_tweaks',
    'home',
    'dashboard',
    'users',
    # 'wallet',
    'tailwind',
    'theme',
]

MIDDLEWARE = [
    'core.middlewares.user_activity_middleware.LogUserIPMiddleware',
    'core.middlewares.bot_blocker.BlockScannersMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    "allauth.usersessions.middleware.UserSessionsMiddleware",
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_NAME', 'postgres_test'),
#         'USER': os.getenv('POSTGRES_USER', 'postgres_test'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres_test'),
#         # Change to your Heroku host
#         'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
#         # Ensure port 5434 is used
#         'PORT': int(os.getenv('POSTGRES_PORT', 5434)),
#     },
# }

DATABASES = {
    # 'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
    'default': dj_database_url.config(default=DATABASE_URL)
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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    # Adjust this path for your app's static files
    os.path.join(BASE_DIR, 'static'),
    # os.path.join(BASE_DIR, 'theme/static'),
]
# Enable WhiteNoise for serving compressed and cached static files
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]
NPM_BIN_PATH = which("npm")

ACCOUNT_FORMS = {
    'login': 'users.forms.CustomLoginForm',
    'signup': 'users.forms.CustomSignupForm',
    'reset_password': 'users.forms.CustomResetPasswordForm',
    'change_password': 'users.forms.CustomChangePasswordForm',
}

SITE_ID = 1

# Email configuration for authentication
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = SMTP_PROVIDER  # e.g., smtp.gmail.com for Gmail
EMAIL_PORT = SMTP_PORT  # Common port for TLS
EMAIL_USE_TLS = True  # Use TLS
EMAIL_HOST_USER = EMAIL_HOST_USER  # Your email address
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD  # Your email password
DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL  # Default from email address


AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",)

ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CHANGE_EMAIL = True
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_BY_CODE_ENABLED = True
USERSESSIONS_TRACK_ACTIVITY = True
SESSION_COOKIE_AGE = 1209600  # Two weeks in seconds (default)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
ACCOUNT_SESSION_REMEMBER = True  # Ensure that the session persists
LOGIN_REDIRECT_URL = "/dashboard/"  # Redirect to the dashboard after login
ACCOUNT_LOGOUT_REDIRECT_URL = 'home'


CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': f'{BASE_DIR}/tmp/django_cache',

    },
}

# LOGGING


# Ensure the log directory exists
LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)-7s %(asctime)s [%(name)s:%(lineno)d] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'level': 'INFO',  # Log INFO level and above
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'django_app.log'),
            'formatter': 'default',
        },
        'error_file': {  # New handler for error logs
            'level': 'ERROR',  # Log ERROR level and above
            'class': 'logging.FileHandler',
            # Separate error log file
            'filename': os.path.join(LOG_DIR, 'django_error.log'),
            'formatter': 'default',
        },
    },
    'root': {
        # Include error_file handler
        'handlers': ['console', 'file', 'error_file'],
        'level': 'INFO',  # Log INFO level and above
    },
    'loggers': {
        'django': {
            # Include error_file handler
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',  # Log INFO level and above
            'propagate': False,
        },
        # Optional: Add a logger for other apps or modules if needed
        # You can customize this section based on your app's structure
        # Example:
        '<your_app_name>': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',  # Log DEBUG level and above for your app
            'propagate': False,
        },
    },
}

# Custom logging for model changes, IP addresses, and user traffic can be handled in views or signals.

# For media in development mode
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
