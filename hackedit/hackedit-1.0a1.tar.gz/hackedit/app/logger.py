"""
This module contains functions for easily setup the application logger
"""
import logging.handlers
import os


def get_path():
    """
    Returns the log file path.

    - GNU/Linux: ``~/.hackedit/hackedit.log``
    - OSX: ``~/Library/Application Support/HackEdit/hackedit.log``
    - WINDOWS: ``%APPDATA%\HackEdit\hackedit.log``

    :return: str
    """
    from hackedit.api import system
    return os.path.join(system.get_app_data_directory(), 'hackedit.log')


def setup(level=logging.INFO):
    """
    Configures the logger, adds a stream handler and a file handler.

    :param level: log level, default is logging.INFO
    """
    handler = logging.handlers.RotatingFileHandler(
            get_path(), maxBytes=2*1024*1024, backupCount=5)
    handlers = [
        # a new log will be created on each new day with 5 days backup
        handler,
        logging.StreamHandler()
    ]
    logging.basicConfig(
        level=logging.WARNING, handlers=handlers,
        format='%(asctime)s:%(msecs)03d::%(levelname)s::%(process)d::%(name)s'
        '::%(message)s', datefmt='%H:%M:%S')
    logging.getLogger().setLevel(level)
    logging.getLogger('hackedit').info('-' * 80)
