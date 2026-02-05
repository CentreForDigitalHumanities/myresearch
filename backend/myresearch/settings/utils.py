from django.core.exceptions import ImproperlyConfigured

import os


def discover(key, default):
    """
    Get a key from os.env with a mandatory default value.
    """
    return os.getenv(key, default)

def discover_list(key, default):
    """
    Get a comma-separated list from os.env with a
    mandatory default value.
    """
    raw = discover(key, "")
    out = [
        item for item in raw.split(",") if item != ""
    [
    return out


def discover_or_fail(key):
    """
    Get a key from os.env or raise an exception if it's missing.
    """
    value = os.getenv(key)
    if value is None:
        raise ImproperlyConfigured(
            f"Couldn't find key {key} in environment.",
        )
    return value
