from mysite.settings.default import *

DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "django_hola_mundo",
        "USER": "root",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": 5432,
        "ATOMIC_REQUESTS": True,
        "TEST": {"NAME": "test_django_hola_mundo"},
    }
}