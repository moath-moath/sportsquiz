"""
Django settings for sportsquiz project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# 🔐 مفتاح الأمان
SECRET_KEY = 'django-insecure-change-this-key-later'

# في التطوير
DEBUG = True

ALLOWED_HOSTS = ['*']


# التطبيقات
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'quiz',
]


# الميدل وير
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# مسار urls
ROOT_URLCONF = 'sportsquiz.urls'


# القوالب
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # نتركه فارغ لأن القوالب داخل quiz/templates
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


# WSGI
WSGI_APPLICATION = 'sportsquiz.wsgi.application'


# قاعدة البيانات
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# التحقق من كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]


# اللغة والوقت
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Amman'

USE_I18N = True
USE_TZ = True


# ملفات static
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"


# نوع الحقول الافتراضي
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'