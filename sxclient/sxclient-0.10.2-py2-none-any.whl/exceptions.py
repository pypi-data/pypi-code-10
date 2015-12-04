'''
Exceptions specific for the package.

Copyright (C) 2012-2015 Skylable Ltd. <info-copyright@skylable.com>
License: Apache 2.0, see LICENSE for more details.

'''

__all__ = [
    'SXClientException', 'InvalidOperationParameter', 'InvalidUserKeyError',
    'SXClusterError', 'SXClusterNotFound', 'SXClusterInternalError',
    'SXClusterFatalError', 'SXClusterNonFatalError'
]


class SXClientException(Exception):
    '''
    General exception type for library-specific exceptions.
    '''


class InvalidOperationParameter(SXClientException):
    '''
    Should be raised when a parameter passed to operation is invalid.
    '''


class InvalidUserKeyError(SXClientException):
    '''
    Should be raised when a user key is invalid.
    '''


class SXClusterError(SXClientException):
    '''
    Should be raised when a problem occurs during communication with the
    cluster.
    '''


class SXClusterFatalError(SXClusterError):
    '''
    Should be raised when the cluster communication problem is fatal.
    '''


class SXClusterNonFatalError(SXClusterError):
    '''
    Should be raised when the cluster communication problem is non-fatal.
    '''


class SXClusterNotFound(SXClusterNonFatalError):
    '''
    Should be raised when cluster responds with 404.
    '''


class SXClusterInternalError(SXClusterNonFatalError):
    '''
    Should be raised when cluster responds with >= 500.
    '''
