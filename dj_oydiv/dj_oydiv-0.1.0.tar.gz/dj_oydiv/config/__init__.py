# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.conf import settings
from django.conf import ImproperlyConfigured

from . import default_settings

log = logging.getLogger(__name__)

__all__ = ['config']

PREFIX = 'OYDIV_'


class _Config(object):
    """
    Allow our app to have some preconfigured defaults, that are overriden
    in the django settings file.
    """

    def __getattr__(self, attr):
        try:
            return getattr(settings, PREFIX + attr)
        except AttributeError:
            try:
                return getattr(default_settings, attr)
            except AttributeError:
                raise ImproperlyConfigured(
                    "The setting '{}' must be defined in django settings.".format(PREFIX + attr)
                )

config = _Config()
