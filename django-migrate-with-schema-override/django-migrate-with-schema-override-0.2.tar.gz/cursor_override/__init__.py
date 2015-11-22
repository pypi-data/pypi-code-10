"""
Django Migrate with Schema Override
~~~~~~~~~~~~~~~~~~
"""
VERSION = (0, 2)
__version__ = VERSION

from time import time

import django
from django.conf import settings
if django.VERSION < (1, 7):
    from django.db.backends import util
else:
    from django.db.backends import utils as util
from django.utils.log import getLogger

def _override_cursor():
    return getattr(settings, 'CURSOR_OVERRIDE', False)

class OverrideCursorWrapper(object):
    """
    This is an override wrapper for a database cursor.

    I need some functionality that migrate will not trip on
    tables with db_name = 'salesforce\".\"sometable' on it
    kudos to:
      - https://github.com/streeter/django-db-readonly
    If I could actually make this to work.
    This is actually v0.2 so my first failed. :P
    """


    def __init__(self, cursor, db):
        self.cursor = cursor
        self.db = db


    def execute(self, sql, params=()):
        self.db.validate_no_broken_transaction()
        with self.db.wrap_database_errors:
            # print('Override SQL: ' + sql)
            sql = sql.replace("_salesforce\".\"","_salesforce_")
            if params is None:
                return self.cursor.execute(sql)
            else:
                return self.cursor.execute(sql, params)


    def executemany(self, sql, param_list):
        self.db.validate_no_broken_transaction()
        with self.db.wrap_database_errors:
            # print('Override SQL: ' + sql)
            sql = sql.replace("_salesforce\".\"","_salesforce_")
            return self.cursor.executemany(sql, param_list)


class CursorWrapper(util.CursorWrapper):
    def __init__(self, cursor, db):
        self.cursor = OverrideCursorWrapper(cursor, db)
        self.db = db


# Redefine CursorDebugWrapper because we want it to inherit from *our*
# CursorWrapper instead of django.db.backends.util.CursorWrapper
class CursorDebugWrapper(CursorWrapper):

    def execute(self, sql, params=()):
        start = time()
        try:
            return self.cursor.execute(sql, params)
        finally:
            stop = time()
            duration = stop - start
            sql = self.db.ops.last_executed_query(self.cursor, sql, params)
            self.db.queries.append({
                'sql': sql,
                'time': "%.3f" % duration,
            })
            logger.debug(
                '(%.3f) %s; args=%s',
                duration, sql, params,
                extra={'duration': duration, 'sql': sql, 'params': params}
            )

    def executemany(self, sql, param_list):
        start = time()
        try:
            return self.cursor.executemany(sql, param_list)
        finally:
            stop = time()
            duration = stop - start
            self.db.queries.append({
                'sql': '%s times: %s' % (len(param_list), sql),
                'time': "%.3f" % duration,
            })
            logger.debug(
                '(%.3f) %s; args=%s',
                duration, sql, param_list,
                extra={'duration': duration, 'sql': sql, 'params': param_list}
            )


if _override_cursor():
    # Monkey Patching!
    util.CursorWrapper = CursorWrapper
    util.CursorDebugWrapper = CursorDebugWrapper