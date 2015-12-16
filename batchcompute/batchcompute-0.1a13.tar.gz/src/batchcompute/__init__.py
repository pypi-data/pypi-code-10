'''A simple implementation of BatchCompute service SDK.
'''
__version__ = '0.1a13'
__all__ = [
    # Client for BatchCompute service.
    "Client",
    # Exceptions.
    "ClientError", "FiledError", "ValidationError", "JsonError", "ConfigError",
    # Available endpoints.
    "CN_QINGDAO", "CN_SHENZHEN"
]
__author__ = 'crisish <helei@alibaba-inc.com>'

from .client import Client
from .core import ClientError, FieldError, ValidationError, JsonError
from .utils import CN_QINGDAO, CN_SHENZHEN, ConfigError
