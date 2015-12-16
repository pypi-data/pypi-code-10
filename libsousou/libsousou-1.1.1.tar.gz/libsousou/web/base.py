import uuid

from libsousou.web.exc import Conflict
from libsousou.web.exc import Forbidden
from libsousou.web.exc import HttpException
from libsousou.web.exc import MethodNotAllowed
from libsousou.web.exc import NotAcceptable
from libsousou.web.exc import NotAuthorized
from libsousou.web.exc import NotFound
from libsousou.web.exc import TemporaryRedirect
from libsousou.web.exc import ServerError
from libsousou.web.exc import ServiceNotAvailable
from libsousou.web.exc import UnprocessableEntity
from libsousou.web.exc import UnsupportedMediaType


class RequestController(object):
    # Errors are attributes so subclasses don't have to import.
    Forbidden = Forbidden
    MethodNotAllowed = MethodNotAllowed
    NotAuthorized = NotAuthorized
    NotFound = NotFound
    UnsupportedMediaType = UnsupportedMediaType
    ServiceNotAvailable = ServiceNotAvailable
    UnprocessableEntity = UnprocessableEntity
    Conflict = Conflict

    #: Enables or disabled strict mode, meaning a rigid enforcement
    #: of HTTP standards.
    strict = False

    #: A list of content types that the controller can provide to the
    #: client. By default, this list is empty, disabling the enforcement.
    #: If strict mode is enabled and accept headers are specified,
    #: the client ``Accept`` header MUST match one or more content
    #: content types specified in this list. If strict mode is
    #: disabled, a warning is logged.
    content_types = []

    #: Specifies a default content type for responses.
    default_content_type = None

    #: The content types the controller will accept.
    allowed_content_types = []

    _authentication_defaults = {
        'GET': True,
        'POST': True,
        'PUT': True,
        'DELETE': True,
        'PATCH': True,
        'HEAD': True,
        'OPTIONS': False,
        'TRACE': True
    }

    #: Indicates if authentication is disabled for the endpoint. May be
    #: a boolean - indicating enable/disable - or a list of HTTP verbs
    #: for which requests should not be authenticated.
    disable_authentication = False

    #: Indicates if authentication through the ``Authorization`` header
    #: is supported.
    enable_www_auth = False

    #: Specifies a relative URL to which the user should be redirected
    #: if not authenticated. If :attr:`enable_www_auth` is ``True`` and
    #: :attr:`login_url` contains a value, the former has precedence.
    login_url = None

    #: Indicates if the controller must operate in debug mode.
    debug = False

    #: The default HTTP status code returned by the endpoint.
    default_status = 200

    @property
    def allowed_methods(self):
        return list(map(str.upper, filter(bool, [getattr(self, x, None)
            for x in ('GET','POST','PUT','DELETE','PATCH','HEAD','OPTIONS','TRACE')])))

    @classmethod
    def as_view(cls, *args, **kwargs):
        def f(*a, **k):
            instance = cls()
            return instance.dispatch(*a, **k)

        #: Indicated that the :meth:`dispatch()` method expects a request
        #: object. This attribute is used for very obscure purposes, and
        #: must always be ``True``
        f.expects_request = True

        # Flask maps the view functions by their __name__ attribute (wtf?)
        # so we assign a unique name.
        f.__name__ = ''.join([cls.__name__, '_', uuid.uuid1().hex])
        return f

    def authenticate(self, request, *args, **kwargs):
        """Authenticate the request or raise a :class:`~libsousou.web.exc.NotAuthorized`
        exception, causing the controller to return a ``401`` response.
        """
        if not self.is_authenticated(request, *args, **kwargs)\
        and self._must_authenticate(request.get_request_method()):
            headers = {}
            if self.enable_www_auth:
                headers['WWW-Authenticate'] = \
                    self.get_authenticate_header(request, *args, **kwargs)

            raise NotAuthorized(headers=headers)\
                if not self.login_url\
                else TemporaryRedirect(self.login_url)

    def get_authenticate_header(self, request, *args, **kwargs):
        """Return the value of the ``WWW-Authenticate`` header. Subclasses may
        override this method to support custom authentication schemes.
        """
        return 'Basic'

    def is_authenticated(self, request, *args, **kwargs):
        """Return a boolean indicating if the incoming request is
        from an authenticated system operator. The default implementation
        always returns ``False``. Ex.:

        Django example:

        .. code:: python

        def is_authenticated(self, request, *args, **kwargs):
            # Assumes that the middleware required by the django.contrib.auth
            # module is enabled.
            return request.user.is_authenticated()
        """
        return False

    def on_server_error(self, exception, request, *args, **kwargs):
        """Invoked on a fatal exception during request processing.

        Is expected to return an object of the same type as returned
        by :meth:`render_to_response()`, with a ``5xx`` status code.
        """
        return ServerError().render_to_response(self.render_to_response, request)

    def dispatch(self, request, *args, **kwargs):
        """Dispatches an incoming request to the appropriate
        hander, based on its HTTP verb.

        Args:
            request: an incoming HTTP request. The object must
                expore a ``get_request_method()`` method, which
                returns a string specifying the request method
                e.g. ``GET``, ``POST``, etc.

        Returns:
            Response

        Raises:
            libsousou.web.exc.MethodNotAllowed: the method specified
                in the request was not allowed.
        """
        method = request.get_request_method()
        try:
            self.authenticate(request, *args, **kwargs)
            handler = self._get_request_handler(method)
            if self.strict:
                self._validate_request(request)
            response = handler(request, *args, **kwargs)
        except HttpException as e:
            response = e.render_to_response(self.render_to_response, request)
        except Exception as e:
            if self.debug:
                raise
            response = self.on_server_error(e, request,  *args, **kwargs)
        return response

    def render(self, context):
        """Renders a context dictionary to the response body."""
        raise NotImplementedError("Subclasses must override this method.")

    def render_to_response(self, context, *args, **kwargs):
        """Renders a :class:`Response` to be sent to the client.

        Args:
            context: a context dictionary to render the content.
            status_code: an integer specifying the status code.
            content_type: a string specifying the returned content
                type.
            headers: a dictionary containing response headers.

        Returns:
            Response
        """
        kwargs['content_type'] = self.default_content_type
        content = self.render(context)
        return self.response_factory(content, *args, **kwargs)

    def _validate_request(self, request):
        if not any(map(request.accepts_content_type, self.content_types))\
        and self.content_types:
            raise NotAcceptable({'accepts': self.content_type})

        if self.strict and self.allowed_content_types\
        and request.content_type not in self.allowed_content_types:
            raise self.UnsupportedMediaType({
                "hint": "This endpoint accepts: {0}."\
                    .format(', '.join(self.allowed_content_types))
            })

    def _get_request_handler(self, method):
        try:
            return getattr(self, method.lower())
        except AttributeError:
            raise MethodNotAllowed(
                headers={'Allow': ', '.join(self.allowed_methods)}
            )

    def _must_authenticate(self, method):
        return not self.disable_authentication \
            if isinstance(self.disable_authentication, bool)\
            else (method.upper() not in self.disable_authentication)
