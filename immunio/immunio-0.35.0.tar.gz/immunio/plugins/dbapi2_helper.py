from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import codecs

from collections import Iterator
from functools import wraps
from itertools import tee
from uuid import uuid4

from immunio.context import get_context
from immunio.exceptions import ImmunioBlockedError
from immunio.logger import log


def wrap_connect(run_hook, original_connect):
    """
    Function to wrap a normal dbapi `connect` functions.
    """

    @wraps(original_connect)
    def connect_wrapper(*args, **kwargs):
        log.debug("dbapi2.connect(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
            })

        connection_uuid = str(uuid4())

        # Convert some class parameters to class names.
        hook_kwargs = dict(kwargs)
        for key in ["factory", "connection_factory", "cursorclass"]:
            if key in hook_kwargs:
                hook_kwargs[key] = hook_kwargs[key].__name__

        # Remove some parameters that don't serialize
        for key in ["conv"]:
            if key in hook_kwargs:
                # Can't encode it, so just remove it for now
                del hook_kwargs[key]

        run_hook("sql_connect", {
            "connection_uuid": connection_uuid,
            "args": args,
            "kwargs": hook_kwargs,
        })

        conn = original_connect(*args, **kwargs)

        return ConnectionWrapper(connection_uuid, run_hook, conn)
    return connect_wrapper


class ConnectionWrapper(object):
    """
    Internal wrapper for a dbapi2 Connection object.

    Note, we're not using inheritance here. If one method uses another,
    we don't want multiple hooks. For instance, if execute() internally
    calls cursor(), we don't want to see both hooks.
    """
    def __init__(self, connection_uuid, run_hook, real_connection):
        self._connection_uuid = connection_uuid
        self._run_hook = run_hook
        self._conn = real_connection

    def __getattr__(self, name):
        """
        If we don't specifically override a method here, pass through
        to the the wrapped Connection.
        """
        # If a non-dbapi2 function is called
        if name in ["execute", "executemany", "executescript"]:
            # And it is present in the real connection
            if hasattr(self._conn, name):
                # Call our wrapped version instead
                return getattr(self, "_" + name)

        return getattr(self._conn, name)

    def __setattr__(self, name, value):
        if name in ['_connection_uuid',
                    '_run_hook',
                    '_conn']:
            object.__setattr__(self, name, value)
        else:
            setattr(self._conn, name, value)

    def __delattr__(self, item):
        if item in ['_connection_uuid',
                    '_run_hook',
                    '_conn']:
            object.__delattr__(self, item)
        else:
            delattr(self._conn, item)

    def cursor(self, *args, **kwargs):
        log.debug("Connection.cursor(%(args)s, %(kwargs)s)", {
            "args": args,
            "kwargs": kwargs,
            })

        cursor_uuid = str(uuid4())

        # Convert some class parameters to class names.
        hook_kwargs = dict(kwargs)
        for key in ["factory", "cursor_factory", "cursorclass"]:
            if key in hook_kwargs:
                hook_kwargs[key] = hook_kwargs[key].__name__

        self._run_hook("sql_cursor", {
            "connection_uuid": self._connection_uuid,
            "cursor_uuid": cursor_uuid,
            "args": args,
            "kwargs": hook_kwargs,
        })
        new_cursor = self._conn.cursor(*args, **kwargs)
        return CursorWrapper(self, cursor_uuid, self._run_hook, new_cursor)

    def _execute(self, sql, params=None):
        params, params_dict = params_to_dict(params)
        log.debug("Connection._execute(%(sql)s, %(params)s)", {
            "sql": sql,
            "params": params,
            })
        strict_context, loose_context, stack, _ = get_context()
        hook_result = self._run_hook("sql_execute", {
            "connection_uuid": self._connection_uuid,
            "sql": sql,
            "params": params_dict,
            "context_key": strict_context,
            "loose_context_key": loose_context,
            "stack": stack,
        })

        if not hook_result.get("allow", True):
            raise ImmunioBlockedError()

        # Some versions of psycopg2 are picky about the value of the default
        # params argument. To avoid any issues, don't pass through params=None.
        if params is None:
            return self._conn.execute(sql)
        else:
            return self._conn.execute(sql, params)

    def _executemany(self, sql, params_list):
        params_list, params_dicts = params_list_to_dicts(params_list)
        log.debug("Connection._executemany(%(sql)s, %(params)s)", {
            "sql": sql,
            "params": params_list,
            })

        strict_context, loose_context, stack, _ = get_context()
        for params_dict in params_dicts:
            hook_result = self._run_hook("sql_execute", {
                "connection_uuid": self._connection_uuid,
                "sql": sql,
                "params": params_dict,
                "context_key": strict_context,
                "loose_context_key": loose_context,
                "stack": stack,
            })

            if not hook_result.get("allow", True):
                raise ImmunioBlockedError()

        return self._conn.executemany(sql, params_list)

    def _executescript(self, sql_script):
        log.debug("Connection._executescript(%(sql_script)s)", {
            "sql_script": sql_script,
            })

        strict_context, loose_context, stack, _ = get_context()
        hook_result = self._run_hook("sql_execute", {
            "connection_uuid": self._connection_uuid,
            "sql_script": sql_script,
            "context_key": strict_context,
            "loose_context_key": loose_context,
            "stack": stack,
        })

        if not hook_result.get("allow", True):
            raise ImmunioBlockedError()

        return self._conn.executescript(sql_script)

    #def create_function(self, name, num_params, func):
    #def create_aggregate(self, name, num_params, aggregate_class):
    #def create_colation(self, name, callable):
    #def interrupt(self):
    #def set_authorizer(self, authorizer_callback):
    #def set_progress_handler(self, handler, n):
    #def enable_load_extension(self, enabled):
    #def load_extension(self, path):
    #row_factory
    #text_factory
    #total_changes
    #def iterdump(self):


class CursorWrapper(object):
    """
    Internal wrapper for a dbapi2 Cursor object.

    Note, we're not using inheritance here. If one method uses another,
    we don't want multiple hooks. For instance, if executemany()
    internally calls execute(), we don't want to see both hooks.
    """
    def __init__(self, connection_wrapper, cursor_uuid, run_hook, real_cursor):
        # Cursor objects require a reference to their connection. We want that
        # reference to point to our wrapped connection.
        self.connection = connection_wrapper

        self._connection_uuid = connection_wrapper._connection_uuid
        self._cursor_uuid = cursor_uuid
        self._run_hook = run_hook
        self._cursor = real_cursor

    def __getattr__(self, name):
        """
        If we don't specifically override a method here, pass through
        to the the wrapped Cursor.
        """
        return getattr(self._cursor, name)

    def __setattr__(self, name, value):
        if name in ['connection',
                    '_connection_uuid',
                    '_cursor_uuid',
                    '_run_hook',
                    '_cursor']:
            object.__setattr__(self, name, value)
        else:
            setattr(self._cursor, name, value)

    def __delattr__(self, item):
        if item in ['connection',
                    '_connection_uuid',
                    '_cursor_uuid',
                    '_run_hook',
                    '_cursor']:
            object.__delattr__(self, item)
        else:
            delattr(self._cursor, item)

    def __iter__(self):
        """
        Implement the cursor iteration protocol by passing to the underlying
        real cursor.
        """
        for result in self._cursor:
            yield result

    def execute(self, sql, params=None):
        params, params_dict = params_to_dict(params)
        log.debug("Cursor.execute(%(sql)s, %(params)s)", {
            "sql": sql,
            "params": params,
            })
        strict_context, loose_context, stack, _ = get_context()
        hook_result = self._run_hook("sql_execute", {
            "connection_uuid": self._connection_uuid,
            "cursor_uuid": self._cursor_uuid,
            "sql": sql,
            "params": params_dict,
            "context_key": strict_context,
            "loose_context_key": loose_context,
            "stack": stack,
        })

        if not hook_result.get("allow", True):
            raise ImmunioBlockedError()

        # Some versions of psycopg2 are picky about the value of the default
        # params argument. To avoid any issues, don't pass through params=None.
        if params is None:
            return self._cursor.execute(sql)
        else:
            return self._cursor.execute(sql, params)

    def executemany(self, sql, params):
        params, params_dict = params_to_dict(params)
        log.debug("Cursor.executemany(%(sql)s, %(params)s)", {
            "sql": sql,
            "params": params,
            })
        strict_context, loose_context, stack, _ = get_context()
        hook_result = self._run_hook("sql_execute", {
            "connection_uuid": self._connection_uuid,
            "cursor_uuid": self._cursor_uuid,
            "sql": sql,
            "params": params_dict,
            "context_key": strict_context,
            "loose_context_key": loose_context,
            "stack": stack,
        })

        if not hook_result.get("allow", True):
            raise ImmunioBlockedError()

        return self._cursor.executemany(sql, params)

    def executescript(self, sql_script):
        log.debug("Cursor.executescript(%(sql_script)s)", {
            "sql_script": sql_script,
            })
        strict_context, loose_context, stack, _ = get_context()
        hook_result = self._run_hook("sql_execute", {
            "connection_uuid": self._connection_uuid,
            "cursor_uuid": self._cursor_uuid,
            "sql_script": sql_script,
            "context_key": strict_context,
            "loose_context_key": loose_context,
            "stack": stack,
        })

        if not hook_result.get("allow", True):
            raise ImmunioBlockedError()

        return self._cursor.executescript(sql_script)


def params_to_dict(params):
    """
    Converts a params list to a dict w/ indexes as names.

    Eg.:

        ['a', 'b'] => {'0': 'a', '1': 'b'}

    Returns a tuple of the original params, in case it was a iterator,
    and a params dict.
    """
    if params is None:
        params_dict = {}

    elif isinstance(params, dict):
        params_dict = params

    else:
        # An iterator can only be consumed once, so never consume from
        # params directly and use tee to consume from a copy instead.
        if isinstance(params, Iterator):
            params_dup, params = tee(params)
        else:
            params_dup = params

        def decode(string):
            if isinstance(string, unicode):
                return string
            elif isinstance(string, (basestring, buffer)):
                return codecs.decode(string, "utf-8", "replace")
            else:
                return unicode(string)

        params_dict = dict((unicode(i), decode(param))
            for i, param in enumerate(params_dup))

    return params, params_dict


def params_list_to_dicts(params_list):
    """
    Convert a list of params list to a list of dicts w/ indexes as names.

    Returns a tuple of the original list of params, in case some of them
    were iterators, and a list of params dicts.
    """
    params_dicts = []
    for i, params in enumerate(params_list):
        params_list[i], params_dict = params_to_dict(params)
        params_dicts.append(params_dict)

    return params_list, params_dicts
