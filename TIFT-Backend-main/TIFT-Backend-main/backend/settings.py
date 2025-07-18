import environ

from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(env_file=BASE_DIR / ".env")
from corsheaders.defaults import default_headers

SECRET_KEY = env.str("SECRET_KEY", default="django-insecure-)uv2xyqk&vk$%67=k)yaf9q-+#!bc3mt#6h(bojwsg+=!3x^oy")

DEBUG = env.bool("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

INSTALLED_APPS = [
    # 'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # third party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "corsheaders",
    "django_apscheduler",
    "modeltranslation",
    "rangefilter",

    # local apps
    "user",
    "university.apps.UniversityConfig",  # <--- THIS
    'tift_bot',
]

JAZZMIN_SETTINGS = {
    "site_title": "TIFT Admin",
    "site_header": "TIFT Admin",
    "site_brand": "TIFT Admin",
    "welcome_sign": "TIFT Qabul tizimi",
    "copyright": "TIFT 2025",

    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],


    "icons": {
        "django_apscheduler.DjangoJob": "fas fa-clock",
        "django_apscheduler.DjangoJobExecution": "fas fa-history",
        "auth.Group": "fas fa-users-cog",
        "auth.User": "fas fa-user-shield",
        "university.Application": "fas fa-book",
        "university.StudentApplication": "fas fa-file-signature",
        "university.Duration": "fas fa-hourglass-half",
        "university.Exam": "fas fa-pencil-alt",
        "university.Faculty": "fas fa-university",
        "university.Program": "fas fa-graduation-cap",
        "university.Question": "fas fa-question-circle",
        "university.StudyType": "fas fa-chalkboard-teacher",
        "university.StudyTypeFaculty": "fas fa-layer-group",
        "university.Subject": "fas fa-book-open",
        "user.OTP": "fas fa-key",
        "user.UserSMS": "fas fa-sms",
        "user.Student": "fas fa-user-graduate",
        "user.User": "fas fa-user",
    },



    "related_modal_active": True,

    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
    },

}

JAZZMIN_UI_TWEAKS = {
    "theme": "lumen",
    "footer_small_text": False,
    "body_small_text": False,
    "theme_switcher": True,

     "brand_colour": "navbar-dark",
    "accent": "accent-lightblue",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "actions_sticky_top": True,
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # User middlewares
    'user.middlewares.is_authentication.UserIsAuthenticationMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (*default_headers, "sentry-trace", "baggage")
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://qabul.tift.uz",
    "https://qabul.tift.uz",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [
            BASE_DIR / "templates",  # e.g., project-level templates dir
        ],
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

WSGI_APPLICATION = "backend.wsgi.application"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'user.custom_JWT.CustomJWTAuthentication',
    )
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB", default="test_db"),
        "USER": env.str("POSTGRES_USER", default="test_user"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", default="test_password"),
        "HOST": env.str("POSTGRES_HOST", default="localhost"),
        "PORT": env.str("POSTGRES_PORT", default="5432")
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),  # Set access token expiration to 1 year
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),  # Optionally set the refresh token lifetime
    'ROTATE_REFRESH_TOKENS': False,
}

LANGUAGE_CODE = "uz"
LANGUAGES = (
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'  # Define the static root

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
TIME_ZONE = "Asia/Tashkent"

USE_I18N = True
USE_L10N = True
USE_TZ = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 1 * 1024 * 1024 * 1024  # 1GB
FILE_UPLOAD_MAX_MEMORY_SIZE = 1 * 1024 * 1024 * 1024  # 1GB
