###############################################################################
#
# Copyright (c) 2007 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""
$Id: __init__.py 4413 2015-11-09 17:05:01Z roger.ineichen $
"""

import os.path

import pymongo

import zope.interface
import zope.component
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.publisher.interfaces import IRequest
from zope.security import management
from zope.security.interfaces import IParticipation
from zope.security.interfaces import IPrincipal
from zope.session.interfaces import IClientId

import m01.fake
import m01.fake.client
import m01.mongo.testing
import m01.stub.testing

import m01.session.client
from m01.session import interfaces


# mongo db name used for testing
TEST_DB_NAME = 'm01_session_testing'
TEST_COLLECTION_NAME = 'test'


###############################################################################
#
# test helper methods
#
###############################################################################

_testClient = None

def getTestClient():
    return _testClient


def getTestDatabase():
    client = getTestClient()
    return client[TEST_DB_NAME]


def getTestCollection():
    database = getTestDatabase()
    return database[TEST_COLLECTION_NAME]


def dropTestDatabase():
    client = getTestClient()
    client.drop_database(TEST_DB_NAME)


def dropTestCollection():
    client = getTestClient()
    client[TEST_DB_NAME].drop_collection(TEST_COLLECTION_NAME)


###############################################################################
#
# Test Component
#
###############################################################################

class Principal(object):
    """Setup principal."""

    zope.interface.implements(IPrincipal)

    id = 'roger.ineichen'
    title = u'Roger Ineichen'
    description = u'Roger Ineichen'


class Participation(object):
    """Setup configuration participation."""

    # also implement IRequest which makes session adapter available
    zope.interface.implements(IParticipation, IUserPreferredLanguages, IRequest)

    def __init__(self, principal, langs=('en', 'de')):
        self.principal = principal
        self.langs = langs
        self.annotations = {}
        self.data = {}

    def get(self, key):
        self.data.get(key)

    def __setitem__(self, key, value):
        self.data[key] = value

    def getPreferredLanguages(self):
        return self.langs

    interaction = None


def startInteraction():
    principal = Principal()
    participation = Participation(principal)
    management.newInteraction(participation)


def endInteraction():
    management.endInteraction()


def setUpSessionClientId():
    namespace = 'm01_session_testing'
    secret = 'very secure'
    cid = m01.session.client.ClientIdFactory(namespace, secret)
    zope.component.provideAdapter(cid, (IRequest,), provides=IClientId)


###############################################################################
#
# test setup methods
#
###############################################################################

# fake mongodb setup
def setUpFakeMongo(test=None):
    """Setup fake (singleton) mongo client"""
    global _testClient
    host = 'localhost'
    port = 45017
    tz_aware = True
    storage = m01.fake.client.DatabaseStorage
    _testClient = m01.fake.FakeMongoClient(host, port, tz_aware=tz_aware,
        storage=storage)


def tearDownFakeMongo(test=None):
    """Tear down fake mongo client"""
    # reset test client
    global _testClient
    _testClient = None


# stub mongodb server
def setUpStubMongo(test=None):
    """Setup pymongo client as test client and setup a real empty mongodb"""
    host = 'localhost'
    port = 45017
    tz_aware = True
    sandBoxDir = os.path.join(os.path.dirname(__file__), 'sandbox')
    import m01.stub.testing
    m01.stub.testing.startMongoDBServer(host, port, sandBoxDir=sandBoxDir)
    # setup pymongo.MongoClient as test client
    global _testClient
    _testClient = pymongo.MongoClient(host, port, tz_aware=tz_aware)


def tearDownStubMongo(test=None):
    """Tear down real mongodb"""
    # stop mongodb server
    sleep = 0.5
    import m01.stub.testing
    m01.stub.testing.stopMongoDBServer(sleep)
    # reset test client
    global _testClient
    _testClient = None
    # clear thread local transaction cache
    m01.mongo.clearThreadLocalCache()
