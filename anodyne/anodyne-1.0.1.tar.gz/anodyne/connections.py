import contextlib
import logging

from anodyne import exceptions
from anodyne import engines

from sqlalchemy import exc as sqla_exc

logger = logging.getLogger(__name__)


def _get_engine(database):
    """
    Convenience function for retrieving a database engine from anodyne.engines.

    :param database: The database to retrieve an engine for.
    :return: a database engine object.
    """
    engine_data = engines.get_engine(database)
    if engine_data is None:
        err = "No engines available for '%s'" % database
        raise exceptions.NoValidEnginesException(err)
    if engine_data.get("engine") is None:
        err = "Engine Data found, but no engine was created. %s" % engine_data
        raise exceptions.EmptyEngineException(err)
    return engine_data


def get_connection(database):
    """
    Retrieves a database connection for the database reference provided.

    :param database: a name of database engine managed by anodyne.
    :return: a connection.
    """
    engine_data = _get_engine(database)
    engine = engine_data.get("engine")
    try:
        conn = engine.connect()
    except sqla_exc.OperationalError, ex:
        logger.exception(
            "Engine failed with error: %r. Switching over." % repr(ex)
        )
        engines.mark_failed(database)
        engine_data = _get_engine(database)
        engine = engine_data.get("engine")
        try:
            conn = engine.connect()
        except sqla_exc.OperationalError:
            engines.mark_failed(database)
            logger.exception("Failed to connect to the database")
            raise
    return conn


@contextlib.contextmanager
def connection(database):
    """
    Context manager for a database connection.

    Used by the:
    with connection("Foo") as conn:
        conn.execute("...")
        ...
    paradigm.

    Begins a database transaction for the requester. Cleans up appropriately
    on error or successful transaction.

    :param database: a name of database engine managed by anodyne.
    :yields: a database connection to the requester.
    """
    conn = get_connection(database)
    transaction = conn.begin()
    try:
        yield conn
    except sqla_exc.OperationalError:
        logger.exception("Failed to execute sql statement.")
        transaction.rollback()
        conn.close()
        raise
    except sqla_exc.DBAPIError:
        logger.exception("Failed to execute transaction.")
        transaction.rollback()
        conn.close()
        raise
    except Exception:
        logger.exception("Unknown exception occurred during transaction.")
        transaction.rollback()
        conn.close()
        raise
    else:
        transaction.commit()
        conn.close()
