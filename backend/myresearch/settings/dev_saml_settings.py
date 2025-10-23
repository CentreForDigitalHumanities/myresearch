from django.urls import reverse_lazy
from os import path
from cdh.federated_auth.saml.settings import *
from .utils import discover
import os

_BASE_DIR = path.dirname(os.path.dirname(__file__))

SAML_CONFIG = create_saml_config(
    base_url=discover("SAML_BASE_URL", "http://localhost:5000/"),
    name="myresearch",
    key_file=path.join(_BASE_DIR, "certs/private.key"),
    cert_file=path.join(_BASE_DIR, "certs/public.cert"),
    idp_metadata=discover(
        "IDP_METADATA_URL", "http://mr-dev-idp:7000/saml/idp/metadata/"
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
