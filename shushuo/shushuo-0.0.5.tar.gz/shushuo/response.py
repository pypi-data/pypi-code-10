

class ShushuoResponse(object):

    def __init__(self, status_code, error_message, result):
        self.success = status_code == 200
        self.status_code = status_code
        self.error_message = error_message
        self.result = result
