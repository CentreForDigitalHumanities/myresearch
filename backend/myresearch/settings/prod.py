from .utils import discover_or_fail

DEBUG = False
SECRET_KEY = discover_or_fail("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = discover_or_fail("DJANGO_ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = discover_or_fail("CSRF_TRUSTED_ORIGINS").split(",")

from .generic_settings import *
