from django.urls import reverse_lazy
from os import path
from cdh.federated_auth.saml.settings import *
from .utils import discover
import os

_BASE_DIR = path.dirname(os.path.dirname(__file__))

SAML_CONFIG = create_saml_config(
    base_url=discover_or_fail("SAML_BASE_URL",),
    name="myresearch",
    key_file="/run/secrets/private.key",
    cert_file="/run/secrets/public.cert",

    # Don't fall back on dev IDP in production, that would be BAD
    idp_metadata=discover_or_fail(
        "IDP_METADATA_URL",
    ),
    contact_given_name="Humanities IT Portal Development",
    contact_email="portaldev.gw@uu.nl",
    allow_unsolicited=True,
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "djangosaml2.backends.Saml2Backend",
)

SAML_ATTRIBUTE_MAPPING = {
    "uuShortID": ("username",),
    "mail": ("email",),
    "givenName": ("first_name",),
    "uuPrefixedSn": ("last_name",),
}
