# coding: utf-8

"""
django informer checker for Database
"""

from django.db import (
    Error, InterfaceError, DatabaseError, DataError, OperationalError,
    IntegrityError, InternalError, ProgrammingError, NotSupportedError
)

from informer.checker.base import BaseInformer, InformerException
from informer.models import Raw


class DatabaseInformer(BaseInformer):
    """
    Database Informer.
    """

    def __str__(self):
        return u'Check if Database is operational.'

    def check(self):
        """
        Inspect default database configuration.
        """
        try:
            Raw.objects.count()
        except (Error, InterfaceError, DatabaseError, DataError,
                OperationalError, IntegrityError, InternalError,
                ProgrammingError, NotSupportedError):
            return False, 'Oh no. Your database is out!'
        except Exception as error:
            raise InformerException(
                'An error occured when trying access database: %s' % error)
        else:
            return True, 'Your database is operational.'
