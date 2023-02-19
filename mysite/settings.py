from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-$l)j4qlz&y8w0p&cdma&*azzd#*xaj^^#15vtf!5dqs&9+du(-"
DEBUG = True
ALLOWED_HOSTS = ["http://127.0.0.1:8000", "127.0.0.1", "http://localhost:5173"]
CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = [
    "Main.apps.MainConfig",
    "corsheaders",
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # добавленный middleware для CORS
    "Main.middlewares.middleware.CustomAuthenticationMiddleware",
    # "Main.middlewares.middleware.CustomPostMiddleware",
]
ROOT_URLCONF = "mysite.urls"
WSGI_APPLICATION = "mysite.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
