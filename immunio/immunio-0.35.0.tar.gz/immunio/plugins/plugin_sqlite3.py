from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from immunio.plugins.dbapi2_helper import wrap_connect


# Name plugin so it can be enabled and disabled.
NAME = "sqli_sqlite"


def add_hooks(run_hook, get_agent_func=None):
    """
    Add hooks to the sqlite3 library.
    """
    try:
        # Some frameworks (notably Django) use the sqlite3.dbapi2 module
        # directly. Others use sqlite3 directly. To cover both cases we
        # have a single wrapper function which we patch onto both references.
        import sqlite3.dbapi2
    except ImportError:
        return None

    meta = {
        "version": sqlite3.dbapi2.version,
        "sqlite_version": sqlite3.dbapi2.sqlite_version,
    }

    # wrap 'sqlite3.dbapi2.connect' function
    wrapped_connect = wrap_connect(run_hook, sqlite3.dbapi2.connect)

    # replace dbapi2 reference to connect
    sqlite3.dbapi2.connect = wrapped_connect
    # replace sqlite3 reference to connect
    sqlite3.connect = wrapped_connect

    return meta
