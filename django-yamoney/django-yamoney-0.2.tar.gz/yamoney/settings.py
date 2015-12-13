# -*- coding: utf-8 -*-
from django.conf import settings as django_settings


def get_setting(name, default):
    """
    A little helper for fetching global settings with a common prefix.
    """
    parent_name = "YAMONEY_{0}".format(name)
    return getattr(django_settings, parent_name, default)

ACCOUNT = get_setting('ACCOUNT', None)
FORM_COMMENT = get_setting('FORM_COMMENT', None)
NOTIFICATION_SECRET = get_setting('NOTIFICATION_SECRET', '')