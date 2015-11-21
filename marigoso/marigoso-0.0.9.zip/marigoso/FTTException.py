class FTTException(Exception):

    def __init__(self, message, status=None):
        super(FTTException, self).__init__(message)
        self.status = status
