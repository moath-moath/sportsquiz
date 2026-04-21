"""
Django settings for sportsquiz project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 مفتاح الأمان
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY', 
    'django-insecure-change-this-key-later'
)

# ⚠️ DEBUG: ضع True للتطوير، False للإنتاج
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    "sportsquiz-1.onrender.com",
    "localhost",
    "127.0.0.1"
]

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
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sportsquiz.urls'

# القوالب
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # القوالب داخل quiz/templates
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

WSGI_APPLICATION = 'sportsquiz.wsgi.application'

# قاعدة البيانات (SQLite للتجربة)
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
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# إعدادات أمان
if DEBUG:
    # أثناء التطوير المحلي، لا نفرض SSL لتجنب ERR_SSL_PROTOCOL_ERROR
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
else:
    # في الإنتاج، تفعيل الأمان الكامل
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# نوع الحقول الافتراضي
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'