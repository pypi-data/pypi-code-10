from anillo.http.responses import Response


def auth_middleware(backend):
    def func_wrapper(func):
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
    return func_wrapper
