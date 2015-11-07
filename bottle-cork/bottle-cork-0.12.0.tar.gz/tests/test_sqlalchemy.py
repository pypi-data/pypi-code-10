# -*- coding: utf-8 -*
# Cork - Authentication module for the Bottle web framework
# Copyright (C) 2013 Federico Ceratto and others, see AUTHORS file.
# Released under LGPLv3+ license, see LICENSE.txt
#
# Functional testing - test the Cork module against diffent database backends

from base64 import b64encode, b64decode
from pytest import raises
import bottle
import mock
import os
import pytest
import time

from cork import Cork, AAAException, AuthException
from cork.backends import JsonBackend
from cork.backends import MongoDBBackend
from cork.backends import SQLiteBackend
from cork.backends import SqlAlchemyBackend
from conftest import assert_is_redirect

import MySQLdb


### Mocked classes

class MockedSession(object):
    """Mock Beaker session
    """
    def __init__(self, username=None):
        self.__username = username
        self.__saved = False

    def get(self, k, default):
        assert k in ('username')
        if self.__username is None:
            return default

        return self.__username

    def __getitem__(self, k):
        assert k in ('username')
        if self.__username is None:
            raise KeyError()

        return self.__username

    def __setitem__(self, k, v):
        assert k in ('username')
        self.__username = v
        self.__saved = False

    def delete(self):
        """Used during logout to delete the current session"""
        self.__username = None

    def save(self):
        self.__saved = True

#TODO: implement tests around MockedSession __saved

class MockedSessionCork(Cork):
    """Mocked Cork instance where the session is replaced with
    MockedSession
    """
    @property
    def _beaker_session(self):
        return self._mocked_beaker_session


### Fixtures and helpers

## Backends

def setup_sqlite_db(request):
    # in-memory SQLite DB using the SQLiteBackend backend module.
    b = SQLiteBackend(':memory:', initialize=True)
    b.connection.executescript("""
        INSERT INTO users (username, email_addr, desc, role, hash, creation_date) VALUES
        (
            'admin',
            'admin@localhost.local',
            'admin test user',
            'admin',
            'cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=',
            '2012-10-28 20:50:26.286723'
        );
        INSERT INTO roles (role, level) VALUES ('special', 200);
        INSERT INTO roles (role, level) VALUES ('admin', 100);
        INSERT INTO roles (role, level) VALUES ('editor', 60);
        INSERT INTO roles (role, level) VALUES ('user', 50);
    """)
    return b


def setup_json_db(request, tmpdir):
    # Setup test directory with valid JSON files and return JsonBackend instance
    tmpdir.join('users.json').write("""{"admin": {"email_addr": "admin@localhost.local", "desc": null, "role": "admin", "hash": "69f75f38ac3bfd6ac813794f3d8c47acc867adb10b806e8979316ddbf6113999b6052efe4ba95c0fa9f6a568bddf60e8e5572d9254dbf3d533085e9153265623", "creation_date": "2012-04-09 14:22:27.075596", "last_login": "2012-10-28 20:50:26.286723"}}""")
    tmpdir.join('roles.json').write("""{"special": 200, "admin": 100, "user": 50, "editor": 60}""")
    tmpdir.join('register.json').write("""{}""")
    return JsonBackend(tmpdir)


def setup_sqlalchemy_with_sqlite_in_memory_db(request):
    # Setup an SqlAlchemyBackend backend using an in-memory SQLite DB

    mb = SqlAlchemyBackend('sqlite:///:memory:', initialize=True)

    ## Purge DB
    mb._drop_all_tables()
    assert len(mb.roles) == 0
    assert len(mb.users) == 0

    # Create roles
    mb.roles.insert({'role': 'special', 'level': 200})
    mb.roles.insert({'role': 'admin', 'level': 100})
    mb.roles.insert({'role': 'editor', 'level': 60})
    mb.roles.insert({'role': 'user', 'level': 50})

    # Create admin
    mb.users.insert({
        "username": "admin",
        "email_addr": "admin@localhost.local",
        "desc": "admin test user",
        "role": "admin",
        "hash": "cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=",
        "creation_date": "2012-10-28 20:50:26.286723",
        "last_login": "2012-10-28 20:50:26.286723"
    })
    assert len(mb.roles) == 4
    assert len(mb.users) == 1

    def fin():
        mb._drop_all_tables()
        assert len(mb.roles) == 0
        assert len(mb.users) == 0

    request.addfinalizer(fin)
    return mb

    #def purge_test_db(self):
    #    # Purge DB
    #    mb = connect_to_test_db()
    #    mb._drop_all_tables()

def setup_mongo_db(request):
    # FIXME no last_login?
    t0 = time.time()
    def timer(s, max_time=None):
        delta = time.time() - t0
        print("%s %f" % (s, delta))
        if max_time is not None:
            assert delta < max_time

    mb = MongoDBBackend(db_name='cork-functional-test', initialize=True)
    timer('connect + init')

    # Purge DB
    mb.users._coll.drop()
    mb.roles._coll.drop()
    mb.pending_registrations._coll.drop()
    timer('purge')

    # Create admin
    mb.users._coll.insert({
        "login": "admin",
        "email_addr": "admin@localhost.local",
        "desc": "admin test user",
        "role": "admin",
        "hash": "cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=",
        "creation_date": "2012-10-28 20:50:26.286723"
    })
    timer('create')

    # Create users
    mb.roles._coll.insert({'role': 'special', 'val': 200})
    mb.roles._coll.insert({'role': 'admin', 'val': 100})
    mb.roles._coll.insert({'role': 'editor', 'val': 60})
    mb.roles._coll.insert({'role': 'user', 'val': 50})
    timer('create users')

    def fin():
        mb.users._coll.drop()
        mb.roles._coll.drop()

    request.addfinalizer(fin)
    timer('mongo setup', 8)
    return mb


def setup_mysql_db(request):

    if os.environ.get('TRAVIS', False):
        # Using Travis-CI - https://travis-ci.org/
        password = ''
        db_name = 'myapp_test'
    else:
        password = ''
        db_name = 'cork_functional_test'

    uri = "mysql://root:%s@localhost/%s" % (password, db_name)
    mb = SqlAlchemyBackend(uri, initialize=True)

    ## Purge DB
    mb._drop_all_tables()

    assert len(mb.roles) == 0
    assert len(mb.users) == 0

    # Create roles
    mb.roles.insert({'role': 'special', 'level': 200})
    mb.roles.insert({'role': 'admin', 'level': 100})
    mb.roles.insert({'role': 'editor', 'level': 60})
    mb.roles.insert({'role': 'user', 'level': 50})

    # Create admin
    mb.users.insert({
        "username": "admin",
        "email_addr": "admin@localhost.local",
        "desc": "admin test user",
        "role": "admin",
        "hash": "cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=",
        "creation_date": "2012-10-28 20:50:26.286723",
        "last_login": "2012-10-28 20:50:26.286723"
    })
    assert len(mb.roles) == 4
    assert len(mb.users) == 1

    def fin():
        return  # TODO: fix
        mb._drop_all_tables()
        assert len(mb.roles) == 0
        assert len(mb.users) == 0

    request.addfinalizer(fin)
    return mb


def setup_postgresql_db(request):

    if os.environ.get('TRAVIS', False):
        # Using Travis-CI - https://travis-ci.org/
        db_name = 'myapp_test'
    else:
        db_name = 'cork_functional_test'

    uri = "postgresql+psycopg2://postgres:@/%s" % db_name
    mb = SqlAlchemyBackend(uri, initialize=True)

    # Purge DB
    mb._drop_all_tables()
    assert len(mb.roles) == 0
    assert len(mb.users) == 0

    # Create roles
    mb.roles.insert({'role': 'special', 'level': 200})
    mb.roles.insert({'role': 'admin', 'level': 100})
    mb.roles.insert({'role': 'editor', 'level': 60})
    mb.roles.insert({'role': 'user', 'level': 50})

    # Create admin
    mb.users.insert({
        "username": "admin",
        "email_addr": "admin@localhost.local",
        "desc": "admin test user",
        "role": "admin",
        "hash": "cLzRnzbEwehP6ZzTREh3A4MXJyNo+TV8Hs4//EEbPbiDoo+dmNg22f2RJC282aSwgyWv/O6s3h42qrA6iHx8yfw=",
        "creation_date": "2012-10-28 20:50:26.286723",
        "last_login": "2012-10-28 20:50:26.286723"
    })
    assert len(mb.roles) == 4
    assert len(mb.users) == 1

    def fin():
        mb._drop_all_tables()
        assert len(mb.roles) == 0
        assert len(mb.users) == 0

    request.addfinalizer(fin)
    return mb



## General fixtures

@pytest.fixture(params=[
    'json',
    'mysql',
    'postgresql',
    'sqlalchemy',
    'sqlite',
])
def backend(tmpdir, request):
    # Create backend instances
    backend_type = request.param
    if backend_type == 'json':
        return setup_json_db(request, tmpdir)

    if backend_type == 'sqlite':
        return setup_sqlite_db(request)

    if backend_type == 'sqlalchemy':
        return setup_sqlalchemy_with_sqlite_in_memory_db(request)

    if backend_type == 'mysql':
        return setup_mysql_db(request)

    if backend_type == 'postgresql':
        return setup_postgresql_db(request)

    raise Exception()


@pytest.fixture
def aaa_unauth(templates_dir, backend):
    # Session without any authenticated user
    aaa = MockedSessionCork(
        templates_dir,
        backend=backend,
        smtp_server='localhost',
        email_sender='test@localhost',
    )
    aaa._mocked_beaker_session = MockedSession()
    return aaa


@pytest.fixture
def aaa_admin(templates_dir, backend):
    # Session with an admin user
    aaa = MockedSessionCork(
        templates_dir,
        backend=backend,
        email_sender='test@localhost',
        smtp_server='localhost',
    )
    aaa._mocked_beaker_session = MockedSession(username='admin')
    return aaa


### Tests

def test_password_hashing(aaa_admin):
    shash = aaa_admin._hash('user_foo', 'bogus_pwd')
    assert len(shash) == 88, "hash length should be 88 and is %d" % len(shash)
    assert shash.endswith(b'='), "hash should end with '='"
    assert aaa_admin._verify_password('user_foo', 'bogus_pwd', shash) == True, \
        "Hashing verification should succeed"


def test_incorrect_password_hashing(aaa_admin):
    shash = aaa_admin._hash('user_foo', 'bogus_pwd')
    assert len(shash) == 88, "hash length should be 88 and is %d" % len(shash)
    assert shash.endswith(b'='), "hash should end with '='"
    assert aaa_admin._verify_password('user_foo', '####', shash) == False, \
        "Hashing verification should fail"
    assert aaa_admin._verify_password('###', 'bogus_pwd', shash) == False, \
        "Hashing verification should fail"


def test_password_hashing_collision(aaa_admin):
    salt = b'S' * 32
    hash1 = aaa_admin._hash(u'user_foo', u'bogus_pwd', salt=salt)
    hash2 = aaa_admin._hash(u'user_foobogus', u'_pwd', salt=salt)
    assert hash1 != hash2, "Hash collision"


@pytest.fixture
def disable_os_urandom(monkeypatch):
    monkeypatch.setattr('os.urandom', lambda n: b'9' * n)


def test_check_hashing(aaa_admin, disable_os_urandom):
    h1 = aaa_admin._hash(u'user', u'pwd')
    assert h1 == b'cDk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5ihNBRY2RYEuI8BWPKndJzD0BTxFOV+hv4Ih9WvRk9Dg='


def test_create_user_check_hashing(aaa_admin, disable_os_urandom):
    assert len(aaa_admin._store.users) == 1, repr(aaa_admin._store.users)
    aaa_admin.create_user(u'phil', 'user', u'pwd')
    assert len(aaa_admin._store.users) == 2, repr(aaa_admin._store.users)
    assert 'phil' in aaa_admin._store.users

    h = aaa_admin._store.users['phil']['hash'].encode('ascii')
    assert h == b'cDk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5OTk5REycUvi9EWiRY7kAUwU4vnGD84a0hstdqigKOaNmqBM='

    assert h == aaa_admin._hash(u'phil', u'pwd')


def test_write_user_hash_bytes(aaa_admin, backend):
    username = 'huh'
    h = b'1234'
    tstamp = "just a string"

    h = h.decode('ascii')
    assert isinstance(h, type(u''))
    aaa_admin._store.users[username] = {
        'role': "user",
        'hash': h,
        'email_addr': "bar",
        'desc': "foo",
        'creation_date': tstamp,
        'last_login': tstamp
    }

    if hasattr(backend, '_engine'):
        h_from_db = backend._engine.execute("SELECT * FROM users").fetchall()[1][2]
        print("H %r" % h_from_db)
        assert h_from_db == '1234'

    fetched_h = aaa_admin._store.users[username]['hash']
    fetched_h = fetched_h.encode('ascii')
    assert isinstance(fetched_h, type(b''))
    assert fetched_h == b'1234'


def test_write_user_hash_unicode(aaa_admin):
    username = 'huh'
    h = u'1234'
    tstamp = "just a string"
    aaa_admin._store.users[username] = {
        'role': "user",
        'hash': h,
        'email_addr': "bar",
        'desc': "foo",
        'creation_date': tstamp,
        'last_login': tstamp
    }

    if hasattr(backend, '_engine'):
        h_from_db = backend._engine.execute("SELECT * FROM users").fetchall()[1][2]
        print("H %r" % h_from_db)
        assert h_from_db == '1234'


    fetched_h = aaa_admin._store.users[username]['hash']
    assert fetched_h == u'1234'


def test_iteritems_on_users(aaa_admin):
    expected_dkeys = set(('hash', 'email_addr', 'role', 'creation_date',
        'desc', 'last_login'))

    if isinstance(aaa_admin._store, MongoDBBackend):
        expected_dkeys.discard('last_login')

    if hasattr(aaa_admin._store.users, 'iteritems'):
        items = aaa_admin._store.users.iteritems()
    else:
        items = iter(aaa_admin._store.users.items())

    for k, v in items:
        dkeys = set(v.keys())

        extra = dkeys - expected_dkeys
        assert not extra, "Unexpected extra keys: %s" % repr(extra)

        missing = expected_dkeys - dkeys
        assert not missing, "Missing keys: %s" % repr(missing)
