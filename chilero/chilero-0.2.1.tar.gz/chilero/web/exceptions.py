from aiohttp import HttpProcessingError


class HttpException(HttpProcessingError):
    pass


class Http400(HttpException):
    code = 400

class Http403(HttpException):
    code = 403

class Http404(HttpException):
    code = 404
