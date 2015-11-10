"""
This module contains utility function used for manipulating the process
environment variables.
"""
import json
import os

from PyQt5 import QtCore

from hackedit.api import system


if system.DARWIN:
    try:
        path = os.environ['PATH']
    except KeyError:
        path = ''
    paths = ['/bin', '/sbin', '/usr/bin', '/usr/sbin', '/usr/local/bin',
             '/usr/local/sbin', '/opt/bin', '/opt/sbin', '/opt/local/bin',
             '/opt/local/sbin'] + path.split(':')
    os.environ['PATH'] = ':'.join(paths)


original_environ = os.environ.copy()


def ignore(k):
    """
    Checks if an environment variable should be ignored by the IDE.

    We ignore variables whose content change when you boot your machine (i.e.
    socket adress, id,...)
    """
    for test in ['_ID', '_ADDRESS', '_SOCK', 'SESSION', 'DISPLAY', 'HACKEDIT']:
        if test in k:
            return True
    return False


def apply():
    """
    Loads environment variables from QSettings and update os.environ
    """
    # update user defined variables
    for k, v in load().items():
        if ignore(k):
            continue
        os.environ[k] = v
    # remove system variables removed by the user
    user_defined = load().keys()
    system_keys = os.environ.keys()
    to_remove = []
    for k in system_keys:
        if ignore(k):
            continue
        if k not in user_defined:
            to_remove.append(k)
    for k in to_remove:
        os.environ.pop(k)
    os.environ['QT_LOGGING_TO_CONSOLE'] = '1'


def restore():
    """
    Restore default environment
    """
    save(dict(original_environ.copy()))
    apply()


def load():
    """
    Loads environment variables from QSettings
    """
    val = json.loads(QtCore.QSettings().value('env/variables', '{}'))
    if not val:
        val = dict(original_environ.copy())
        save(val)
    return val


def save(env):
    """
    Saves the environement variables dict to QSettings and update os.environ.
    """
    value = json.dumps(env)
    QtCore.QSettings().setValue('env/variables', value)
