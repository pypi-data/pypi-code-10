

class BaseError(Exception):

    def __str__(self):
        # all sub-classes should set self._message in their initializers
        return self._message


class InvalidEventError(BaseError):

    def __init__(self, message):
        super(InvalidEventError, self).__init__()

        self.message = message
        self._message = "Invalid event: {0}".format(message)


class InvalidProfileError(BaseError):

    def __init__(self, message):
        super(InvalidProfileError, self).__init__()

        self.message = message
        self._message = "Invalid profile: {0}".format(message)


class InvalidQueryError(BaseError):

    def __init__(self, message):
        super(InvalidQueryError, self).__init__()

        self.message = message
        self._message = "Invalid query: {0}".format(message)
