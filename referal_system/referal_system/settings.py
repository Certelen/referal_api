import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WEB_HOST = os.getenv(
    'WEB_HOST', default='127.0.0.1')
WEB_PORT = os.getenv(
    'WEB_PORT', default='')
SECRET_KEY = os.getenv(
    'SECRET_KEY', default='dwocqp(h%yrd&yrtl-u2qo)p@sphb&1@-&svm6p8g-gzf3h9xo')

DEBUG = False

ALLOWED_HOSTS = ['*']


AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'djoser',
    'users',
    'referals',
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

ROOT_URLCONF = 'referal_system.urls'

CSRF_TRUSTED_ORIGINS = [f"http://{WEB_HOST}:{WEB_PORT}"]

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

# WSGI_APPLICATION = 'referal_system.wsgi.application'
ASGI_APPLICATION = 'referal_system.asgi.application'


EMAIL_HOST = os.getenv(
    'EMAIL_HOST', default='smtp.yandex.ru')
EMAIL_PORT = os.getenv(
    'EMAIL_PORT', default=465)
EMAIL_HOST_USER = os.getenv(
    'EMAIL_HOST_USER', default='dst98@yandex.ru')
EMAIL_HOST_PASSWORD = os.getenv(
    'EMAIL_HOST_PASSWORD', default='xtutrxgriazvvect')
EMAIL_USE_SSL = os.getenv(
    'EMAIL_USE_SSL', default=True)
EMAIL_USE_TLS = os.getenv(
    'EMAIL_USE_SSL', default=False)

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME', default='postgres'),
        'USER': os.getenv('DATABASE_USERNAME', default='postgres'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', default='postgres'),
        'HOST': os.getenv('DATABASE_HOST', default='db'),
        'PORT': os.getenv('DATABASE_PORT', default='5432'),
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'SEARCH_PARAM': 'name',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user_create': 'users.serializers.PostUserCreateSerializer',
        'user': 'users.serializers.PostUserCreateSerializer',
        'current_user': 'users.serializers.GetUserSerializer',
    },
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'activation': ['djoser.permissions.IsAdminUser'],
        'password_reset': ['rest_framework.permissions.AllowAny'],
        'password_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'set_password': ['djoser.permissions.CurrentUserOrAdmin'],
        'username_reset': ['rest_framework.permissions.AllowAny'],
        'username_reset_confirm': ['rest_framework.permissions.AllowAny'],
        'set_username': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_create': ['rest_framework.permissions.AllowAny'],
        'user_delete': ['djoser.permissions.CurrentUserOrAdmin'],
        'user': ['djoser.permissions.CurrentUserOrAdmin'],
        'user_list': ['djoser.permissions.CurrentUserOrAdmin'],
    }}

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
