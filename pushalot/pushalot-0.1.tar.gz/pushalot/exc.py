class PushalotException(Exception):
    """
    Base Exception class.
    """

class PushalotInvalidAPIKey(Exception):
    """
    Raised if invalid token used
    """

class PushalotBadRequestException(PushalotException):
    """
    Input data validation failed
    """

class PushalotNotAcceptableException(PushalotException):
    """
    Message throttle limit hit.
    """

class PushalotGoneException(PushalotException):
    """
    The AuthorizationToken is no longer valid and
    no more messages should be ever sent again using that token.
    """

class PushalotInternalErrorException(PushalotException):
    """
    Service internal server error (HTTP 500).
    """

class PushalotUnavailableException(PushalotException):
    """
    Pushalot servers is overloaded with requests.
    """