# coding=utf8
from __future__ import unicode_literals

import six


def ensure_unicode(content):
    if content is None:
        return content
    elif six.PY2:
        return '{}'.format(content)
    elif isinstance(content, bytes):
        # python3
        return content.decode('utf-8')

    return content
