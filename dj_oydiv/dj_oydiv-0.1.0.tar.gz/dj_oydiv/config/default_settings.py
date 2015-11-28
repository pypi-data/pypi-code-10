# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from importlib import import_module as _import


"""
The settings here are all sensible defaults, but can be overriden in settings.py
"""

# Allow the django project to decide on sensible defaults for crypto
CRYPTO_KDF_ITERATIONS = _import('django.contrib.auth.hashers').PBKDF2PasswordHasher.iterations
DEFAULT_PASSWORD_LENGTH = 32

# Defaults used in creating members on the portal.
DEFAULT_GROUP_NAME = 'Default'
DEFAULT_ROLE_NAME = 'Normal'
DEFAULT_PROXY_NAME = 'No Proxy'
DEFAULT_LOCATION_TAG = 'Default'
# The portal will reject this email. It must overridden.
DEFAULT_MANAGER_EMAIL = 'root@localhost'

# dictionary of passwords keyed by username used to authenticate a portal
# attemping webservices authentication.
# see views.wsauth.
WSAUTH_PORTAL_CREDENTIALS = {}
