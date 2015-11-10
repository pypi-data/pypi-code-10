import functools

from anillo.http.responses import Response

from .backends.http_auth import HttpBasicAuthBackend


def wrap_auth(func=None, *, backend=HttpBasicAuthBackend):
    """
    A middleware that adds the auth management to the
    request.

    This middleware optionally accepts a `backend` keyword
    only parameter for provide the authentication
    implementation. If it is not provided, the http basic
    auth backend will be used.

    :param backend: A backend factory/constructor.
    :type backend: callable or class
    """

    if func is None:
        return functools.partial(wrap_auth, backend=backend)

    # Initialize the storage
    backend = backend()

    def wrapper(request):
        data = backend.parse(request)

        if isinstance(data, Response):
            return data

        if data:
            request = backend.authenticate(request, data)

            if isinstance(request, Response):
                return request

        return func(request)
    return wrapper
