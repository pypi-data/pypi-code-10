#!/usr/local/bin/python
# coding: utf-8
__author__ = 'spouk'

__all__ = ['Database']


import peewee
from peewee import *

from flask_peewee.exceptions import ImproperlyConfigured
from flask_peewee.utils import load_class


class Database(object):
    """init database  and make hook before/after for disable fucking error --> 2006, 'MySQL server has gone away
        database access in context application in app.db
        struct application for avoid mutual imports, example:
        ---
        config.py
        ---------
            # ---------------------------------------------------------------------------
            #   MYSQL config
            # ---------------------------------------------------------------------------
            MYSQL_HOST = 'localhost'
            MYSQL_NAME = 'bottle'
            MYSQL_PORT = 3306
            MYSQL_USER = 'anonym'
            MYSQL_PASSWD = 'anonympassword'
            MYSQL_DB_MAX_CONNECTION = 100
            MYSQL_STALE_TIMEOUT = 20
            MYSQL_ENGINE = 'playhouse.pool.PooledMySQLDatabase'

            DATABASE_MYSQL = {
                'name': MYSQL_NAME,
                'engine': MYSQL_ENGINE,
                'user': MYSQL_USER,
                'passwd': MYSQL_PASSWD,
                'port': MYSQL_PORT,
                'max_connections': MYSQL_DB_MAX_CONNECTION,
                'stale_timeout': MYSQL_STALE_TIMEOUT
            }

        model.py - create database class, define models database use in project
        --------
            from peewee import *
            import config
            from spouk_bottle_peewee import Database


            db = Database(database_config=config.DATABASE_MYSQL)

            class Sucker(db.Model):
                id = PrimaryKeyField()
                username = TextField(default=None)
                password = TextField(default=None)
                status = BooleanField(default=False)

        app.py - create app = Bottle(), import from  model.py db=Database(...), app.install(db)
        ------
            from model import db
            from bottle import Bottle, template

            app = Bottle()
            app.install(db)

        views.py
        --------
        from app import app
        from model import Sucker



        @app.get('/listsuckers, name='listsuckers')
        def suck():
            lsuck= Sucker.select().where(Sucker.status)
            return jinja2_template('users.html', users=lsuck)


        users.html
        ----------
        {% if users %}
            {% for user in users %}
            {{ user.id }} {{user.username}} {{ user.password }} {{ user.status }} <br/>
            {% endfor %}
        {% endif %}

        ----
        a brief example of the use, enjoy
        in fact, variations in the use and application within the bottle is large enough to
        describe this here, practice and experiments to achieve the desired goals you

    """

    name = 'spouk_bottle_peewee'
    api = 2

    def __init__(self, database_config):
        self.database_config = database_config
        self.app = None
        self.initdatabase()
        self.Model = self.get_model_class()

    def setup(self, app):
        self.app = app
        self.app.db= self
        self.app.add_hook('before_request', self.connect_db)
        self.app.add_hook('after_request', self.close_db)


    def apply(self,callback, context):
        return callback

    def initdatabase(self):
        try:
            self.dbname = self.database_config.pop('name')
            self.db_engine = self.database_config.pop('engine')
        except KeyError:
            raise ImproperlyConfigured('Please specify a "name" and "engine" for your database')
        try:
            self.database_class = load_class(self.db_engine)
            assert issubclass(self.database_class, peewee.Database)
        except ImportError:
            raise ImproperlyConfigured('Unable to import: "%s"' % self.db_engine)
        except AttributeError:
            raise ImproperlyConfigured('Database engine not found: "%s"' % self.db_engine)
        except AssertionError:
            raise ImproperlyConfigured('Database engine not a subclass of peewee.Database: "%s"' % self.db_engine)

        self.database = self.database_class(self.dbname, **self.database_config)

    def get_model_class(self):
        class BaseModel(Model):
            class Meta:
                database = self.database

        return BaseModel

    def connect_db(self):
        self.database.connect()

    def close_db(self):
        if not self.database.is_closed():
            self.database.close()


