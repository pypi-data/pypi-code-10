class SocketLabsException(Exception):
    def __init__(self, response, msg=None):
        self.response = response
        super(SocketLabsException, self).__init__(msg)

class SocketLabsUnauthorized(SocketLabsException):
    # HTTP 401: Unauthorized
    def __init__(self, response):
        self.errors = 'Unauthorized'
        self.problem = 'Unauthorized'
        super(SocketLabsUnauthorized, self).__init__(response, 'Check values for username and password')
