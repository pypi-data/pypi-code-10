from __future__ import absolute_import, unicode_literals

import functools
import logging

from django.core.exceptions import PermissionDenied

logger = logging.getLogger(__name__)


def _printfn(fn, alternative, *args):
    warning = '%s %s is deprecated. Use %s instead' % (
        str(fn.__class__) + '.', str(fn.__name__) + '()', alternative
    )
    s = ''.join([str(arg) + ' ' for arg in args])
    logger.warn('[DEPRECATION WARNING]:%s, %s', warning, s)


def deprecated_method(method, alternative=None, warnfn=_printfn):
    @functools.wraps(method)
    def _wrapped(obj=None, *args, **kwargs):
        warnfn(method, alternative)
        if obj:
            return method(obj, *args, **kwargs)
        return method(*args, **kwargs)
    return _wrapped


def permission_denied_wrapper(method):
    @functools.wraps(method)
    def _wrapped(*args, **kwargs):
        logger.warn("permission to access %r(*%r, **r)" % (
            method, args, kwargs)
        )
        raise PermissionDenied()
    return _wrapped
