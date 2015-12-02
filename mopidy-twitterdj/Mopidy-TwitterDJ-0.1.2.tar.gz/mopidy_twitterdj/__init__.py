from __future__ import unicode_literals

import logging
import os

# TODO: Remove entirely if you don't register GStreamer elements below
import pygst
pygst.require('0.10')
import gst
import gobject

from mopidy import config, ext


__version__ = '0.1.2'

# TODO: If you need to log, use loggers named after the current Python module
logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-TwitterDJ'
    ext_name = 'twitterdj'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['consumerkey'] = config.String()
        schema['consumersecret'] = config.Secret()
        schema['token'] = config.String()
        schema['secret'] = config.Secret()
        schema['username'] = config.String()
        schema['playlist'] = config.String()
        return schema

    def setup(self, registry):
        from .frontend import TwitterDJFrontend
        registry.add('frontend', TwitterDJFrontend)
