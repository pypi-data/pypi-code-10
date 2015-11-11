###############################################################################
#
# Copyright (c) 2010 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""
$Id: tests.py 4413 2015-11-09 17:05:01Z roger.ineichen $
"""
__docformat__ = "reStructuredText"

import unittest
import doctest

import m01.mongo.testing

from m01.searcher import interfaces
from m01.searcher import criterion
from m01.searcher import filter
from m01.searcher import testing


# ISearchCriterion
class TestSearchCriterion(m01.mongo.testing.MongoSubItemBaseTest):

    def getTestInterface(self):
        return interfaces.ISearchCriterion

    def getTestClass(self):
        return criterion.SearchCriterion


# ISearchFilterStorage
class FakeSearchFilterStorage(filter.SearchFilterStorage):
    """Search filter with dummy collection"""

    @property
    def collection(self):
        return None


class TestSearchFilterStorage(m01.mongo.testing.MongoStorageBaseTest):

    def getTestInterface(self):
        return interfaces.ISearchFilterStorage

    def getTestClass(self):
        return FakeSearchFilterStorage

    def makeTestObject(self):
        return FakeSearchFilterStorage()


# ISearchFilter
class TestSearchFilter(m01.mongo.testing.MongoItemBaseTest):

    def getTestInterface(self):
        return interfaces.ISearchFilter

    def getTestClass(self):
        return filter.SearchFilter


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('README.txt',
            setUp=testing.setUpFakeMongo, tearDown=testing.tearDownFakeMongo,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        doctest.DocFileSuite('README.txt',
            setUp=testing.setUpStubMongo, tearDown=testing.tearDownStubMongo,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
            ),
        unittest.makeSuite(TestSearchCriterion),
        unittest.makeSuite(TestSearchFilterStorage),
        unittest.makeSuite(TestSearchFilter),
        ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
