from pathlib import Path
import os
import environ

import pymysql
pymysql.install_as_MySQLdb()

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env.read_env(str(BASE_DIR / ".env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api",
    "core",
    "admins",
    "rest_framework",
    "corsheaders",
    "easy_thumbnails",
    "django_filters",
    "colorfield",  # "debug_toolbar",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "b_tex.middleware.LoginRequiredMiddleware",
]

ROOT_URLCONF = "b_tex.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "b_tex.language_context_processor.language_context",
            ],
        },
    },
]

WSGI_APPLICATION = "b_tex.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_database_name',
        'USER': 'root',  # Или твой пользователь
        'PASSWORD': '',  # Пароль, если установлен
        'HOST': '127.127.126.50',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

AUTH_PASSWORD_VALIDATORS: list = list()

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True

STATIC_URL = env("STATIC_URL")
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, env("ADMIN_STATIC")),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = env("MEDIA_URL")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

THUMBNAIL_ALIASES = {
    "": {
        "400x400": {"size": (400, 400), "crop": False},
        "ten": {"size": (200, 200), "crop": False},
        "1100x1100": {"size": (1100, 1100), "crop": False},
        "btn_img": {"size": (50, 50), "crop": False},
        "avatar": {"size": (90, 90), "crop": False},
        "1500x700": {"size": (1500, 700), "crop": False},
        "900x900": {"size": (900, 900), "crop": False},
        "1500x1500": {"size": (1500, 1500), "crop": False},
    },
}


THUMBNAIL_PRESERVE_EXTENSIONS = "webp"
THUMBNAIL_EXTENSION = "webp"
THUMBNAIL_TRANSPARENCY_EXTENSION = "webp"


LOGIN_REDIRECT_URL = "/admin/applications"
LOGOUT_REDIRECT_URL = "/admin/login"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "core.pagination.BasePagination",
    "DATE_INPUT_FORMATS": [
        ("%Y.%m.%d"),
    ],
    "DATETIME_FORMAT": "%H:%m | %d.%m.%Y",
    "DATE_FORMAT": "%d.%m.%Y",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
}


CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "Language",
]


INTERNAL_IPS = [
    "127.0.0.1",
]  # for debug toolbar

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'C:/Users/User/Documents/admin.b-tex.eu-master/cache',  # Абсолютный путь
    }
}


SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


BOT_TOKEN = env("BOT_TOKEN")
CHAT_ID = env("CHAT_ID")
