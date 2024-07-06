from datetime import timedelta
from os import path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-)kbi)f$_*cfhhzaiyjlt+)0n+*fzsmnou+!or0az7&s@qw#qm%'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'drf_spectacular',
    'rest_framework',
    'django_jalali',
    'rest_framework_simplejwt',
    'ckeditor',
    'ckeditor_uploader',
    'easy_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts.apps.AccountsConfig',
    'apps.planing.apps.PlaningConfig',
    'apps.blog.apps.BlogConfig',
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

ROOT_URLCONF = 'resumeApiProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'resumeApiProject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'resume_api',
        'USER': 'root',
        'PASSWORD': '8730310248m',
        'OPTIONS': {
            'autocommit': True
        }
    }
}

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

LANGUAGE_CODE = 'fa-ir'
TIME_ZONE = 'Asia/Tehran'
USE_TZ = True

USE_I18N = True

CKEDITOR_UPLOAD_PATH = 'ckeditor/upload_files/'
CKEDITOR_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Link', 'Unlink', 'Image'],
        ]
    },
    'special': {
        'toolbar': 'Special',
        'height': 200,
        'toolbar': 'full',
        'toolbar_Special': [
            ['Bold', 'Italic', 'Underline', 'Link', 'Unlink', 'Image'],
            ['CodeSnippet'],

        ], 'extraPlugins': ','.join(['codesnippet', 'clipboard'])
    },
    'special_an': {
        'toolbar': 'Special',
        'height': 200,
        'toolbar_Special': [
            ['Bold'],
            ['CodeSnippet'],
        ], 'extraPlugins': ','.join(['codesnippet', 'clipboard'])
    }
}

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = path.join(BASE_DIR, 'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'apps.utilities.CustomPagination',
    'PAGE_SIZE': 25,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Online Resume Project API',
    'DESCRIPTION': 'Rest Api for Online Resume',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
