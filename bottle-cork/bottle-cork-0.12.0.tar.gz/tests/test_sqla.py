

from sqlalchemy import create_engine, delete, select, \
    Column, ForeignKey, Integer, MetaData, String, Table, Unicode

from cork.backends import SqlAlchemyBackend
import pytest
import os
from cork import Cork

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

@pytest.fixture
def backend(tmpdir, request):
    return setup_postgresql_db(request)

    raise Exception()

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

def test_write_user_hash_bytes(aaa_admin):
    username = 'huh'
    h = b'1234'
    tstamp = "just a string"

    assert isinstance(h, type(b''))
    aaa_admin._store.users[username] = {
        'role': "user",
        'hash': h,
        'email_addr': "bar",
        'desc': "foo",
        'creation_date': tstamp,
        'last_login': tstamp
    }

    #eng = aaa_admin._store._engine
    #print(eng.execute("SELECT * FROM users").fetchall()[1])

    fetched_h = aaa_admin._store.users[username]['hash']
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

    fetched_h = aaa_admin._store.users[username]['hash']
    eng = aaa_admin._store._engine
    print(eng.execute("SELECT * FROM users").fetchall()[1])
    assert fetched_h == u'1234'
