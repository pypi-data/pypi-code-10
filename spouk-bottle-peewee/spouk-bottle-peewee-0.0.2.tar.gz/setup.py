#!/usr/bin/env python

import sys
import os
from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

files = ['spouk_bottle_peewee/*']
setup(
    name = 'spouk-bottle-peewee',
    version = '0.0.2',
    url = 'http://spouk.ru',
    description = 'orm peewee integrating plugin for bottle',
    long_description = """init database  and make hook before/after for disable fucking error --> 2006, 'MySQL server has gone away
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
        ---
        Copyleft [x] 2015, Spouk
    """,
    author = 'Spouk',
    author_email = 'spouk@spouk.ru',
    license = 'MIT',
    platforms = 'any',
     packages=['spouk_bottle_peewee'],
    package_data = {'spouk_bottle_peewee': files},
    
    py_modules = [
        'spouk_bottle_peewee'
    ],
    requires = [
        'bottle (>=0.9)',
        'peewee (>=2.6.3)',
    ],
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    cmdclass = {'build_py': build_py}
)

