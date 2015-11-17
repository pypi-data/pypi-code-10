class NotZippedError(Exception):
    """Exception for unzipped sources"""
    def __init__(self, message):
        super(NotZippedError, self).__init__(message)
        self.message = message

class NotIndexedError(Exception):
    """Exception for unzipped sources"""
    def __init__(self, message):
        super(NotIndexedError, self).__init__(message)
        self.message = message
        