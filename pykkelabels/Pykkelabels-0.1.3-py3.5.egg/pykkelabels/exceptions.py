class HTTPError(Exception):
    def __init__(self, message):
        super(HTTPError, self).__init__(message)


class URLError(Exception):
    def __init__(self, message):
        super(URLError, self).__init__(message)