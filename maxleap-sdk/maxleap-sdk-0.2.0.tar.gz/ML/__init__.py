# coding: utf-8

"""MaxLeap Python SDK
"""

import client
from .client import init, by_hook, change_region, UserPrincipal, get_master_principal
from .errors import MaxLeapError
from .object_ import Object
from .query import Query
from .relation import Relation
from .server import Server, get_principal
from .log import Log
from flask import Response

__author__ = 'czhou <czhou@ilegendsoft.com>'
__version__ = '0.1.16'
DEBUG = True
PRO = False

__all__ = [
    'MaxLeapError',
    'Object',
    'Query',
    'Relation',
    'client',
    'init',
    'by_hook',
    'change_region',
    'UserPrincipal',
    'get_master_principal',
    'Server',
    'get_principal',
    'Log',
    'Response'
]
