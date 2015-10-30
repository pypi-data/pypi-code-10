class PageError(Exception):
    def __init__(self, message):
        super(PageError, self).__init__(message)


class ConnError(Exception):
    def __init__(self, message):
        super(ConnError, self).__init__(message)