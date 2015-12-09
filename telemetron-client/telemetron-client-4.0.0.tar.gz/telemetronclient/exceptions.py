"""
Telemetron Exception classes.
"""


class TelemetronClientException(Exception):
    """
    Base class for every Telemetron Client exception
    """
    pass


class TransportNotInitialized(TelemetronClientException):
    """
    TransportNotInitialized class
    """
    pass


class TelemetronValueError(TelemetronClientException):
    """
    TelemetronValueError class
    """
    pass
