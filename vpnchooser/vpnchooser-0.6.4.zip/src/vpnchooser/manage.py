# -*- encoding: utf-8 -*-
"""
Manager for the application.
"""

import sys
from getpass import getpass

from flask.ext.script import Manager
from celery.bin.worker import worker

from vpnchooser.applicaton import app, celery
from vpnchooser.syncer import sync as do_sync
from vpnchooser.db import db, session, User
from vpnchooser.cli import (
    ConfigurationGenerator,
    DockerConfigurationGenerator,
)


manager = Manager(app)


def _init_app(config=None):
    if config is None:
        app.config.from_envvar('FLASK_CONFIG_FILE')
    else:
        app.config.from_pyfile(config)
    celery.conf.update(app.config)
    celery.conf['BROKER_URL'] = app.config['CELERY_BROKER_URL']


@manager.command
@manager.option('-c', '--config', dest='config', default=None)
@manager.option('-h', '--host', dest='host', default=None)
@manager.option('-p', '--port', dest='port', default=None)
def runserver(config=None, host=None, port=None):
    _init_app(config)
    app.run(host=host, port=int(port))


@manager.command
@manager.option('-c', '--config', dest='config', default=None)
def init_db(config=None):
    _init_app(config)
    db.create_all()


@manager.command
@manager.option('-c', '--config', dest='config', default=None)
def sync(config=None):
    _init_app(config)
    do_sync()
    print("Synchronization complete")


@manager.command
@manager.option('-c', '--config', dest='config', default=None)
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_admin(username, password, config=None):
    _init_app(config)
    user = User()
    user.name = username
    user.password = password
    user.is_admin = True
    user.generate_api_key()
    session.add(user)
    session.commit()


@manager.command
@manager.option('-c', '--config', dest='config', default=None)
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password', default=None)
def reset_password(username, password=None, config=None):
    _init_app(config)
    user = session.query(User).filter(User.name == username).first()
    if user is None:
        print('User %s not found' % username)
    if password is None:
        password = getpass('Enter new password: ')

    user.password = password
    session.commit()
    print('Password reset done for user %s' % username)


@manager.command
@manager.option('-c', '--config', dest='config', default=None)
def runcelery(config=None):
    _init_app(config)
    # Fix for setuptools generated scripts, so that it will
    # work with multiprocessing fork emulation.
    # (see multiprocessing.forking.get_preparation_data())
    if __name__ != '__main__':  # pragma: no cover
        sys.modules['__main__'] = sys.modules[__name__]
    from billiard import freeze_support

    freeze_support()
    worker(app=celery).run_from_argv('vpnchooser', argv=[
        '-B'
    ])


@manager.command
@manager.option(
    '-c',
    '--config',
    help='file location the config should be written to.'
)
@manager.option(
    '--docker',
    default=False,
    dest='docker',
    action='store_true',
    help='Wether the configuration should be populated by the default '
         'docker data.'
)
def generate_config(config, docker=False):
    if docker:
        generator = DockerConfigurationGenerator(config)
    else:
        generator = ConfigurationGenerator(config)
    generator.generate()


def main():
    manager.run()


if __name__ == '__main__':
    main()
