import copy

from libsousou.web.rfc2616 import *


class HttpException(Exception):
    status = None
    default_context = {}

    def __init__(self, context=None, headers=None):
        self.headers = headers or {}
        self.context = copy.deepcopy(self.default_context)
        self.context.update(context or {})

    def render_to_response(self, render_to_response, request):
        """Renders the appropriate response for the :class:`HttpException`.

        Args:
            render_to_response: a response factory.

        Returns:
            libsousou.web.IResponse
        """
        return render_to_response(self.context, headers=self.headers,
            status_code=self.status)


class TemporaryRedirect(HttpException):
    status = 307

    def __init__(self, url, *args, **kwargs):
        self.url = url
        HttpException.__init__(self, *args, **kwargs)



class BadRequest(HttpException):
    status = 400
    default_context = {
        "code": "BAD_REQUEST",
        "message": (
            "The request could not be understood by the server due to "
            "malformed syntax. The client SHOULD NOT repeat the request without "
            "modifications."
        )
    }


class NotAuthorized(HttpException):
    status = 401
    default_context = {
        "code": "NOT_AUTHORIZED",
        "message": "The request required user authentication.",
        "detail": (
            "RFC 2616: The request requires user authentication. "
            "The response MUST include a WWW-Authenticate header "
            "field (section 14.47) containing a challenge applicable "
            "to the requested resource. The client MAY repeat the request "
            "with a suitable Authorization header field (section 14.8). "
            "If the request already included Authorization credentials, "
            "then the 401 response indicates that authorization has been "
            "refused for those credentials. If the 401 response contains "
            "the same challenge as the prior response, and the user agent "
            "has already attempted authentication at least once, then the "
            "user SHOULD be presented the entity that was given in the "
            "response, since that entity might include relevant diagnostic "
            "information."
        )
    }


class Forbidden(HttpException):
    status = 403
    default_context = {
        "code": "FORBIDDEN",
        "message": "The server understood the request, but is refusing to fulfill it.",
        "detail": (
            "RFC 2616: The server understood the request, but is refusing to fulfill it. "
            "Authorization will not help and the request SHOULD NOT be repeated. If the "
            "request method was not HEAD and the server wishes to make public why the "
            "request has not been fulfilled, it SHOULD describe the reason for the "
            "refusal in the entity. If the server does not wish to make this "
            "information available to the client, the status code 404 (Not Found) "
            "can be used instead."
        )
    }


class MethodNotAllowed(HttpException):
    status = 405
    default_context = {
        "code": "METHOD_NOT_ALLOWED",
        "message": (
            "The method specified in the Request-Line is not allowed "
            "for the resource identified by the Request-URI."
        )
    }

class NotFound(HttpException):
    status = 404
    default_context = {
        "code": "RESOURCE_DOES_NOT_EXIST",
        "message": (
            "The server has not found anything matching the Request-URI."
        )
    }


class NotAcceptable(HttpException):
    status = 406
    default_context = {
        "code": "NOT_ACCEPTABLE",
        "message": (
            "The resource identified by the request is only capable of generating "
            "response entities which have content characteristics not acceptable "
            "according to the accept headers sent in the request."
        )
    }


class Conflict(HttpException):
    status = 409
    default_context = {
        "code": "DUPLICATE_RESOURCE",
        "message": "The request could not be completed due to a conflict with the current state of the resource.",
        "detail": ""
    }


class UnsupportedMediaType(HttpException):
    status = 415
    default_context = {
        "code": "UNSUPPORTED_MEDIA_TYPE",
        "message": "The Content-Type of the request is not understood.",
        "detail": (
            "The server is refusing to service the request because the "
            "entity of the request is in a format not supported by the "
            "requested resource for the requested method."
        )
    }


class UnprocessableEntity(HttpException):
    status = 422
    default_context = {
        "code": "UNPROCESSABLE_ENTITY",
        "message": (
            "The server understands the content-type of the request entity "
            "and the syntax of the request entity is correct "
            "but was unable to process the contained instructions."
        )
    }


class ServerError(HttpException):
    status = 500
    default_context = {
        "code": "SERVER_ERROR",
        "message": "The server encountered an unexpected condition which prevented it from fulfilling the request."
    }


class ServiceNotAvailable(HttpException):
    status = 503
    default_context = {
        "code": "SERVICE_NOT_AVAILABLE",
        "message": "The server is currently unable to handle the request."
    }
