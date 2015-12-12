class SyncGatewayError(Exception):
    pass


class NoDatabaseSpecifiedError(Exception):

    def __str__(self):
        return "No database specified"


class ResponseError(SyncGatewayError):

    def __init__(self, prefix, status, message):
        self.prefix = prefix
        self.status = status
        self.message = message

    def __str__(self):
        return "{prefix}: {status} : {message}".format(
            prefix=self.prefix,
            status=self.status,
            message=self.message
        )


class UnexpectedResponseError(ResponseError):

    def __init__(self, status, message):
        super(UnexpectedResponseError, self).__init__(
            "Unexpected http error", status, message
        )
