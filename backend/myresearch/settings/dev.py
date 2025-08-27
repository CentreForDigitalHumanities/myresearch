from .utils import discover

DEBUG = True
SECRET_KEY = "django-insecure-s8e=1!*6dzct5!vn$0%qdc!x4$_vhd895g0a1#e$_v+oqbvvyq"

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "mr-django",
    "[::1]",
]

INTERNAL_IPS = ["127.0.0.1"]


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5000",
] + discover("CSRF_TRUSTED_ORIGINS", [])

from .generic_settings import *

try:
    from .local_settings import *
except ImportError:
    print(
        "No local settings found. You can put local Django settings "
        "in myresearch/settings/local_settings.py and Django will "
        "load them when running the dev profile."
    )
