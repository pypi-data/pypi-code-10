class ExpresslyError(Exception):
    def __init__(self,
                 message=None,
                 http_body=None,
                 http_status=None,
                 json_body=None,
                 headers=None):
        super(ExpresslyError, self).__init__(message)

        self.message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}


class GenericError(ExpresslyError):
    pass


class AuthenticationError(ExpresslyError):
    pass


class CustomerRegistrationFailedError(ExpresslyError):
    pass


class CustomerAlreadyExistsError(ExpresslyError):
    pass


class UuidError(ExpresslyError):
    pass


class InvalidRequestDataError(ExpresslyError):
    pass


class InvalidApiKeyError(ExpresslyError):
    pass


class InvalidHTMLError(ExpresslyError):
    pass
