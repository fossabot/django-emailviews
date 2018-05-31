import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# custom settings for test
SETTINGS_DICT = dict(
    EXPIRATION_TIME=40000,
    ROOT_URLCONF="tests.urls",
    INSTALLED_APPS=[
        "emailviews",
        "tests",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
    ],
    MIDDLEWARE=[
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ],
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(BASE_DIR, "templates")],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ],
    DATABASES={
        "default": {"ENGINE": "django.db.backends.sqlite3"},
        # 'default': {
        #     'ENGINE': 'django.db.backends.postgresql',
        #     'NAME': postgres_settings['POSTGRES_DB'],
        #     'USER': postgres_settings['POSTGRES_USER'],
        #     'PASSWORD': postgres_settings['POSTGRES_PASSWORD'],
        #     'HOST': 'localhost',
        #     'PORT': postgres_settings['POSTGRES_PORT'],
        # }
    },
)
