"""
Django DB Readonly
~~~~~~~~~~~~~~~~~~
"""
VERSION = (0, 1)
__version__ = VERSION

from time import time

import django
from django.conf import settings
if django.VERSION < (1, 7):
    from django.db.backends import util
else:
    from django.db.backends import utils as util
from django.utils.log import getLogger


class OverrideCursorWrapper(object):
    """
    This is an override wrapper for a database cursor.

    I need some functionality that migrate will not trip on
    tables with db_name = 'salesforce\".\"sometable' on it
    kudos to:
      - https://github.com/streeter/django-db-readonly
    If I could actually make this to work. XD
    """


    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db


    def execute(self, sql, params=()):
        self.db.validate_no_broken_transaction()
        with self.db.wrap_database_errors:
            print('Override SQL: ' + sql)
            sql = sql.replace("_salesforce\".\"","_salesforce_")
            if params is None:
                return self.cursor.execute(sql)
            else:
                return self.cursor.execute(sql, params)


    def executemany(self, sql, param_list):
        self.db.validate_no_broken_transaction()
        with self.db.wrap_database_errors:
            print('Override SQL: ' + sql)
            sql = sql.replace("_salesforce\".\"","_salesforce_")
            return self.cursor.executemany(sql, param_list)


class CursorWrapper(util.CursorWrapper):
    def __init__(self, cursor, db):
        self.cursor = OverrideCursorWrapper(cursor, db)
        self.db = db


