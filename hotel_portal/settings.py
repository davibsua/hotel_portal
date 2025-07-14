"""
Django settings for hotel_portal project
"""

from pathlib import Path
import os
import dj_database_url
from django.urls import reverse_lazy

# ──────────────────────────────────────────────
#  BASE & SECRET
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-87_sbc=r=uhdb7%9t7oa1vw7h_k#cu=uhi)8dk)skax)c@f58k"

CSRF_TRUSTED_ORIGINS = [
    'https://hotel-portal.onrender.com',
]


DEBUG = True            # ponlo en False en producción

ALLOWED_HOSTS = [
    "hotel-portal.onrender.com",
    "localhost",
    "127.0.0.1",
]

# Permitir hosts extra desde variable de entorno (opcional)
extra_hosts = os.environ.get("EXTRA_ALLOWED_HOSTS", "")
if extra_hosts:
    ALLOWED_HOSTS += [h.strip() for h in extra_hosts.split(",")]

# ──────────────────────────────────────────────
#  APPS
# ──────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "empleados",
]

# ──────────────────────────────────────────────
#  MIDDLEWARE
# ──────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",   # sirve estáticos en producción
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hotel_portal.urls"

# ──────────────────────────────────────────────
#  TEMPLATES
# ──────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],                # añade rutas de plantillas externas si las tienes
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "hotel_portal.wsgi.application"

# ──────────────────────────────────────────────
#  DATABASES
# ──────────────────────────────────────────────
# Usará Postgres si DATABASE_URL existe.  De lo contrario, SQLite local.
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=bool(os.environ.get("DATABASE_URL")),   # SSL solo si estamos en Postgres remoto
    )
}

# ──────────────────────────────────────────────
#  PASSWORD VALIDATION
# ──────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ──────────────────────────────────────────────
#  INTERNATIONALIZATION
# ──────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────
#  STATIC FILES
# ──────────────────────────────────────────────
STATIC_URL  = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"                    # carpeta generada por collectstatic

STATICFILES_DIRS = [
    BASE_DIR / "empleados" / "static",                    # tus archivos estáticos de desarrollo
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ──────────────────────────────────────────────
#  AUTH / LOGIN
# ──────────────────────────────────────────────
AUTH_USER_MODEL = "empleados.Usuario"
LOGIN_URL         = reverse_lazy("login")
LOGIN_REDIRECT_URL = "/panel/"

# ──────────────────────────────────────────────
#  DEFAULT PRIMARY KEY
# ──────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
