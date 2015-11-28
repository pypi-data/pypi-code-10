from __future__ import absolute_import, unicode_literals

import logging
import functools

from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist

from .basic import http_basic_credentials as basic_auth
from .basic import HttpResponseBasicChallenge

from ..utils.request import get_client_ip

logger = logging.getLogger(__name__)


def vidyo_admin_rpc_auth(view, auth_fn=basic_auth, fail_class=HttpResponseBasicChallenge):
    """django view decorator that attempts to authenticate an RPC call with
    the django standard login methods, and supplying the vidyo admin user as an
    attribute of the request object, and decrypt the admin's encrypted rpc
    credentials. Views will then be able to do the following.:

    >>> def myview(request)
        try:
            request.user.vidyoadmin.some_field
        except (AttributeError) as e:
            print("No Videos for you!:%r", e)

    `auth_fn` (if given) is expected to return a tuple of the (username, password)
    for the user.

    `fail_class` is any callable that returns an HttpResponse suitable for the
    failure. This could simply be `HttpResponeForbidden`, or similar. The only
    requirement is that it returns an HttpRespone.
    It is called with a single string argument of the reason for failure.
    """

    @functools.wraps(view)
    def fn(request, *args, **kwargs):
        try:
            username, password = auth_fn(request)
        except (AttributeError, ValueError):
            return fail_class("Forbidden")

        if not request.user.is_authenticated():
            logger.debug(" user '%s' was not authenticated", request.user)
            request.user = authenticate(username=username, password=password)
            if request.user is not None:
                if request.user.is_active:
                    login(request, request.user)
                else:
                    logger.debug(" user '%s' is not active", request.user)
                    return fail_class("Forbidden")
            else:
                logger.debug("Anonymous user was not authenticated", request.user)
                return fail_class("Forbidden")
        try:
            request.user.vidyoadmin.decrypt(password)
        except (ValueError, ObjectDoesNotExist):
            return fail_class("Forbidden")
        if not request.user.vidyoadmin.is_ip_allowed(get_client_ip(request)):
            logger.debug("Access from disallowed IP address:%s", get_client_ip(request))
            return fail_class("Forbidden")
        logger.info("Vidyo auth allowed for user '%s'", request.user)

        return view(request, *args, **kwargs)

    return fn
