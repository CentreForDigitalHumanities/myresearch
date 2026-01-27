from .utils import discover_or_fail

DEBUG = False
SECRET_KEY = discover_or_fail("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = discover_or_fail("DJANGO_ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = discover_or_fail("CSRF_TRUSTED_ORIGINS").split(",")

from .generic_settings import *

# SAML STUFF
try:
    from .prod_saml_settings import *

    # Only add the required apps/middleware if we could load the SAML config
    INSTALLED_APPS += SAML_APPS
    MIDDLEWARE += SAML_MIDDLEWARE

    LOGOUT_REDIRECT_URL = "/"
    LOGIN_REDIRECT_URL = "/"

except Exception as e:
    print("Proceeding without SAML")
    print("Exception:", e)
