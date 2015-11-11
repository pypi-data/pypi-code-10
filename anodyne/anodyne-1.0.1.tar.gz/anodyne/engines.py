import logging
import os
import urlparse

from sqlalchemy import exc as sqla_exc
from sqlalchemy import create_engine as sqla_create_engine
from sqlalchemy import pool as sqla_pool
from sqlalchemy import orm

from anodyne import exceptions as _exceptions


logger = logging.getLogger(__name__)
engines = {}
failure_callbacks = {}


def setup_engine(backend_name, verbose=False):
    """
    Read configuration values from the environment and attempt to piece them
    together in order to initiate a connection pool to our database.

    A full database URL can be provided as:
      - ANODYNE_<backend-name>_URL=<database-url>

    If a full URL is not provided, each component must be provided individually:
      - ANODYNE_<backend-name>_DRIVER=<driver type (e.g. sqlite, psycopg2, etc).>
      - ANODYNE_<backend-name>_NAME=<database-name>
      - ANODYNE_<backend-name>_HOST=<database-host>
      - ANODYNE_<backend-name>_PORT=<database-port>
      - ANODYNE_<backend-name>_USER=<database-username>
      - ANODYNE_<backend-name>_PASS=<database-password>

    When the environment is incorrectly configured, this will raise a
    ConfigurationException error.

    :param backend_name: the name of a backend we should discover in the env.
    """
    engine_data = engines.get(backend_name)
    if engine_data is not None:
        return

    prefix = "_".join(["anodyne", backend_name]).upper()
    url_key = "_".join([prefix, "url"]).upper()
    db_url = os.environ.get(url_key)
    if not db_url:
        env_vars = ["driver", "name", "host", "port", "user", "pass"]
        try:
            values = dict(
                (key, os.environ["_".join([prefix, key]).upper()])
                for key in env_vars
            )
        except KeyError:
            err = "Invalid database configuration. Please check your environment."
            raise _exceptions.ConfigurationException(err)
        auth = "%s:%s" % (values["user"], values["pass"])
        host = "%s:%s" % (values["host"], values["port"])
        url_parts = (
            values["driver"],
            "@".join([auth, host]),
            values["name"],
            None,
            None
        )
        db_url = urlparse.urlunsplit(url_parts)
    split = urlparse.urlsplit(db_url)
    kwargs = {
        "poolclass": sqla_pool.QueuePool,
        "logging_name": ".".join([__name__, backend_name]),
        "echo": verbose
    }
    scheme = split.scheme
    if scheme.startswith("sqlite"):
        connect_args = kwargs.get("connect_args", {})
        connect_args.update({"check_same_thread": False})
        kwargs["connect_args"] = connect_args
    engine = sqla_create_engine(db_url, **kwargs)
    engine_data = {
        "engine": engine,
        "name": backend_name,
        "session_class": orm.sessionmaker(bind=engine),
        "failed": False
    }
    engines[backend_name] = engine_data


def scan():
    """
    Scan the ANODYNE_BACKENDS envvar and look for a list of defined data
    backends.
    """
    backends = os.environ.get("ANODYNE_BACKENDS", "")
    for backend in backends.split(","):
        setup_engine(backend)


def register_failure_callback(backend_name, failure_callback):
    failure_callbacks[backend_name] = failure_callback


def poke_engine(engine_meta_data, attempt):
    """
    "Poking" an engine. Meaning attempting a connection on said engine in order
    to revive it's health status (failed => False).

    This function is useful for periodic health checks on a given engine,
    as well as recovery of a dead engine. It will call the global callback
    function `failure_callback`, in the event that the connection fails.

    It is useful to configure this as something such as "gevent.spawn_later",
    using this function as the callback.

    :param engine_meta_data: the engine_meta_data to check.
    :param attempt: how many times we've already poked this engine.
    """
    if len(engines.keys()) == 0:
        err = "Tried to poke engine: %s but no engines are " \
              "defined." % backend_name
        raise _exceptions.ConfigurationException(err)

    if not backend_name in engine.keys():
        err = "Tried to poke engine: %s but could not find engine " \
              "data." % backend_name
        logger.error(err)
        return

    engine_meta_data = engines[backend_name]
    engine = engine_meta_data.get("engine")
    logger.info("Poking engine: %r. This is attempt: %d" % (
        repr(engine), (attempt + 1)
    ))
    try:
        conn = engine.connect()
        conn.close()
        engines[backend_name]["failed"] = False
        logger.info("Engine revived.")
    except sqla_exc.OperationalError:
        logger.warning(
            "Poked %r, but it still appears to be down." % repr(engine)
        )
        failure_callback = failure_callbacks.get(engine_meta_data["name"])
        if on_engine_failure is not None:
            on_engine_failure(engine_meta_data, attempt + 1)


def mark_failed(backend_name):
    """
    Marks a given engine as failed, If the failure callback is defined, it will
    be executed with the engine object.

    :param backend_name: a db name mapping to connection engine meta data.
    :param engine: engine metadata that should have a reference to.
    """
    if len(engines.keys()) == 0:
        err = "Tried to mark: %s failed but no engines are " \
              "defined." % backend_name
        raise _exceptions.ConfigurationException(err)

    if not backend_name in engines.keys():
        err = "Tried to mark: %s failed but could not find engine " \
              "data." % backend_name
        logger.error(err)
        return


    engine_data = engines.get(backend_name)

    if engine_data is None:
        logger.error("No engines configured for: %s." % backend_name)
        return

    engines[backend_name]["failed"] = True
    on_engine_failure = failure_callbacks.get(backend_name)
    if on_engine_failure is not None:
        on_engine_failure(engine, 0)


def get_engine(backend_name):
    """
    Retrieves a sqlalchemy Engine object to use for database connections.

    :param backend_name: a db name mapping to connection engine meta data.
    :return: engine meta data used to create a connection.
    """
    if len(engines.keys()) == 0:
        err = "Tried to get engine for: %s but no engines " \
              "configured." % backend_name
        raise _exceptions.ConfigurationException(err)
    if not backend_name in engines.keys():
        err = "Tried to get engine for: %s but could not find " \
              "engine data." % backend_name
        logger.error(err)
        return

    engine_data = engines.get(backend_name)
    if not engine_data["failed"]:
        return engine_data
    return None


def clean_engines(backend_name=None):
    """
    Disposes of all listed engines mapped to by backend_name.
    If backend_name is empty, we clear them all.

    :param backend_name: a db name mapping to connection engine meta data.
    """
    if backend_name is None:
        for key in engines.keys():
            del engines[key]
            if key in failure_callbacks:
                del failure_callbacks[key]
        return

    if backend_name in engines:
        del engines[backend_name]
    if backend_name in failure_callbacks:
        del failure_callbacks[backend_name]
