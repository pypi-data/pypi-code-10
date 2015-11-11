###############################################################################
#
# Copyright (c) 2010 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""
$Id: testing.py 4413 2015-11-09 17:05:01Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import zope.interface
import zope.schema
from zope.publisher.interfaces import IRequest

import p01.memcache.testing
import p01.session.testing

import m01.mongo.interfaces
import m01.mongo.item
import m01.mongo.schema
import m01.mongo.storage
import m01.mongo.testing
from m01.mongo.fieldproperty import MongoFieldProperty


import m01.searcher.criterion
import m01.searcher.filter
import m01.searcher.session
from m01.searcher import interfaces


class ISampleStorage(m01.mongo.interfaces.IMongoStorage):
    """Sample storage interface."""


class SampleStorage(m01.mongo.testing.TestCollectionMixin,
    m01.mongo.storage.MongoStorage):
    """Sample storage."""

    zope.interface.implements(ISampleStorage)

    def __init__(self):
        pass

    def load(self, data):
        """Load data into the right mongo item."""
        return SampleContent(data)


class ValueCriterion(m01.searcher.criterion.SearchCriterion):
    """Value search criterion"""

    title = u'My Value Search'

    @property
    def updateQuery(self, query):
        if self.connector == interfaces.OR:
            query = {'$and': [query, {'value': self.value}]}
        elif self.connector == interfaces.AND:
            query['value'] = self.value
        elif self.connector == interfaces.NOT:
            query['value'] = {'$ne': self.value}


class SampleSearchFilter(m01.searcher.filter.SearchFilter):
    """Sample search filter"""

    criterionFactories = {'values': ValueCriterion}


class ISampleSearchSession(interfaces.ISearchSession):
    """SampleSearchSession"""


class SampleSearchSession(m01.searcher.session.SearchSession):

    zope.interface.implementsOnly(ISampleSearchSession)

    def load(self, data):
        return SampleSearchFilter(data)


def setUpFakeMongo(test):
    m01.mongo.testing.setUpFakeMongo(test)
    p01.memcache.testing.setUpFakeMemcached(test)
    p01.session.testing.setUpMemcacheClientId()
    p01.session.testing.setUpSession()


def tearDownFakeMongo(test):
    m01.mongo.testing.tearDownFakeMongo(test)
    p01.memcache.testing.tearDownFakeMemcached(test)


def setUpStubMongo(test):
    m01.mongo.testing.setUpStubMongo(test)
    p01.memcache.testing.setUpFakeMemcached(test)
    p01.session.testing.setUpMemcacheClientId()
    p01.session.testing.setUpSession()


def tearDownStubMongo(test):
    m01.mongo.testing.tearDownStubMongo(test)
    p01.memcache.testing.tearDownFakeMemcached(test)
