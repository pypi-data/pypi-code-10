import logging

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_variables
from django.core.exceptions import PermissionDenied
from django.utils.crypto import constant_time_compare
from django.utils.lru_cache import lru_cache
from django.utils.encoding import force_text
from django.contrib.auth import authenticate

from spyne.decorator import srpc
from spyne.service import ServiceBase
from spyne.model.primitive import Boolean, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView
from spyne.application import Application

from ..auth.basic import http_basic_credentials, HttpResponseBasicChallenge
from ..utils.request import get_client_ip
from ..config import config

logger = logging.getLogger(__name__)


__all__ = [
    "portal_wsauth_as_view", "settings_portal_authenticator",
    "deny_all"
]


# The class generation here is expensive, so cache its return value.
@lru_cache()
def portal_wsauth_as_view(user_authenticator, portal_authenticator):
    """
    Create a view that validates a user login request from a portal.
    ``portal_authenticator`` and ```user_authenticator`` are both callbacks
    to functions taking two positional arguments, (``username``, ``password``)
    ```user_authenticator`` authenticates a user against the Portal.
    ``portal_authenticator`` validates whether the VidyoPortal itself is allowed
    to request validation for a particular user (essentially acting like an API key).

    Authentication callbacks should avoid setting cookies, or actually authenticating
    a user to the system, but simply check the user/password combination is valid
    to avoid leaving uneccessary sessions lying around.

    e.g.
    >>> from django.contrib.auth.models import User

    >>> def my_callback(username, password):
    ...     try:
    ...         user = User.objects.get(username=username)
    ...         if not user.is_active or not user.is_staff:
    ...             return False
    ...         return user.check_password(password)
    ...     except User.DoesNotExist:
    ...         return False

    """
    @sensitive_variables('username', 'password')
    def authenticator_wrapper(callback):
        """
        Close over the original callback with a simple exception handling wrapper
        to protect against inadvertent information leakage in case the supplied
        callback gets its knickers in a twist, and raises something like ``DoesNotExist``
        which will subsequently be marshalled into a 500 rather than returning False.
        That situation will allow for very easy object fingerprinting from remote.
        We don't want it.
        """
        def inner(username, password):
            try:
                return callback(username, password)
            # Catching bare ``Exception`` here
            except Exception as e: # NOQA
                logger.exception("user callback failed with exception:%s", e)
                return False

        return inner

    user_authenticator = authenticator_wrapper(user_authenticator)
    portal_authenticator = authenticator_wrapper(portal_authenticator)

    class VidyoPortalAuthSoapView(DjangoView):
        """
        Checks the user/password header sent as part of the HTTP basic auth
        request against the user's VidyoPortal validator, before dispatching
        to the Spyne SOAP handler.
        """
        @sensitive_variables('username', 'password')
        def dispatch(self, request, *args, **kwargs):
            # Vidyo sends the credentials in the HTTP_AUTHORIZATION header
            if request.META['REQUEST_METHOD'] == 'POST':
                try:
                    username, password = map(
                        force_text, http_basic_credentials(request)
                    )
                except (AttributeError, ValueError):
                    return HttpResponseBasicChallenge()
                if not portal_authenticator(username, password):
                    logger.info(
                        "failed authentication for '%s' from %s ",
                        username,
                        get_client_ip(request)
                    )
                    return HttpResponseBasicChallenge()

            return super(VidyoPortalAuthSoapView, self).dispatch(request, *args, **kwargs)

    return VidyoPortalAuthSoapView.as_view(
        application=Application([
            type(
                'AuthenticationService',
                (ServiceBase,),
                {
                    'AuthenticationRequest': srpc(
                        Unicode,
                        Unicode,
                        _returns=Boolean,
                        _out_message_name='AuthenticationResponse',
                        _out_variable_name='passed'
                    )(user_authenticator)
                }
            )],
            tns='http://ws.vidyo.com/authentication',
            in_protocol=Soap11(validator='lxml'),
            out_protocol=Soap11()
        )
    )


@sensitive_variables()
def settings_portal_authenticator(username, password):
    """
    Check an incoming portal webservices authentication request against
    a user and password from the project's settings.py
    ``settings.OYDIV_WSAUTH_CREDENTIALS``, should be a dictionary-like object of
    password values indexed by username.
    """
    try:
        return constant_time_compare(config.WSAUTH_PORTAL_CREDENTIALS[username], password)
    except KeyError:
        logger.info("rejected portal auth request for %r", username)
        return False


_deny = lambda u, p: False


deny_all = csrf_exempt(
    portal_wsauth_as_view(_deny, settings_portal_authenticator)
)
deny_all.__doc__ = (
    """
    A default deny policy for all incoming authentication requests.
    The Portal itself is verified using ``settings_portal_authenticator``.
    This is usefaul if you're handling all endpoint authentication yourself with
    the webservices API, and will provide users an extra barrier to accessing
    their account configuration on the portal.
    """
)


def _django_auth_validator(staff_only):
    def inner(username, password):
        try:
            user = authenticate(username=username, password=password)
        except PermissionDenied:
            return False
        if not user:
            return False
        if user.is_anonymous():
            return False
        if staff_only and not user.is_staff:
            return False
        if user.is_active:
            return True
        return False

    return inner


django_auth_staffonly_view = csrf_exempt(
    portal_wsauth_as_view(_django_auth_validator(staff_only=True), settings_portal_authenticator)
)
django_auth_staffonly_view.__doc__ = (
    """
    Try and authenticate a user with ``django.contrib.auth``.
    If the user is not a staff member, the portal authentication
    will be denied.

    Portal SOAP calls are validated with ``settings_portal_authenticator``
    """
)

django_auth_user_view = csrf_exempt(
    portal_wsauth_as_view(_django_auth_validator(staff_only=False), settings_portal_authenticator)
)
django_auth_user_view.__doc__ = (
    """
    Try and authenticate a user with the `django.contrib.auth`.
    Portal SOAP calls are validated with ``settings_portal_authenticator``.
    """
)
