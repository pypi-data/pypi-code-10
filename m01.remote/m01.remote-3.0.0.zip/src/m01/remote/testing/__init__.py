###############################################################################
#
# Copyright (c) 2011 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
###############################################################################
"""Testing
$Id:$
"""
__docformat__ = "reStructuredText"

import os
import logging
import time

import pymongo

import zope.component
from zope.schema import ValidationError

import m01.fake
import m01.fake.client
import m01.mongo.testing
import m01.stub.testing

from m01.remote import job
from m01.remote import exceptions
from m01.remote.processor import RemoteProcessor


# mongo db name used for testing
TEST_DB_NAME = 'm01_remote_testing'


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


###############################################################################
#
# Testing stubs
#
###############################################################################

class EchoJob(job.Job):
    """A simple echo, job implementation."""

    def __call__(self, remoteProcessor):
        return self.input


class SleepJob(job.Job):
    """Sleep job."""

    def __call__(self, remoteProcessor):
        (sleepTime, id) = self.input
        time.sleep(sleepTime)
        log = logging.getLogger('m01.remote')
        log.info('Job: %i' %id)


class RemoteExceptionJob(job.Job):
    """A simple RemoteException job for testing."""

    def __call__(self, remoteProcessor):
        raise exceptions.RemoteException('An error occurred.')


class FatalExceptionJob(job.Job):
    """A fatal exception for testing"""

    def __call__(self, remoteProcessor):
        raise ValidationError('An error occurred.')


testCounter = 0

class TransactionAbortJob(job.Job):
    """A job which counts and calls transaction.abort for testing"""

    def __call__(self, remoteProcessor):
        log = logging.getLogger('m01.remote')
        log.info('Job: %i' % self.input)

        global testCounter
        testCounter += 1

        import transaction
        transaction.abort()


class TestProcessor(RemoteProcessor):
    """RemoteProcessor used for testing hwihc knows our test jobs"""

    def getRemoteProcessorDB(self):
        return getTestDatabase()

    # job item loader
    def loadRemoteProcessorJobItems(self, data):
        """Load data into the relevant item type"""
        _type = data.get('_type')
        if _type == 'EchoJob':
            obj = EchoJob(data)
        elif _type == 'SleepJob':
            obj = SleepJob(data)
        elif _type == 'RemoteExceptionJob':
            obj = RemoteExceptionJob(data)
        elif _type == 'FatalExceptionJob':
            obj = FatalExceptionJob(data)
        elif _type == 'TransactionAbortJob':
            obj = TransactionAbortJob(data)
        else:
            raise TypeError("No class found for mongo _type %s" % _type)
        return obj


###############################################################################
#
# testing setup
#
###############################################################################
from zope.testing.loggingsupport import InstalledHandler


testProcessor  = None

def setUpTestProcessor():
    """Hook up our TestSite instance"""
    global testProcessor
    testProcessor = TestProcessor()
    return testProcessor

def tearDownTestProcessor():
    """Tear down our TestSite instance"""
    global testProcessor
    testProcessor.stopProcessor()
    testProcessor.stopScheduler()
    testProcessor = None

def setUpSchedulerClassTest():
    """Hook up our TestSite instance"""
    setUpFakeMongo()
    global testProcessor
    testProcessor = TestProcessor()
    return testProcessor

def tearDownSchedulerClassTest():
    """Tear down our TestSite instance"""
    global testProcessor
    testProcessor.stopProcessor()
    testProcessor.stopScheduler()
    testProcessor = None
    tearDownFakeMongo()


# fake mongodb setup used for instance testing
def setUpFakeMongo(test=None):
    """Setup fake (singleton) mongo client"""
    global _testClient
    host = 'localhost'
    port = 45017
    storage = m01.fake.client.DatabaseStorage
    _testClient = m01.fake.FakeMongoClient(host, port, storage=storage)


def tearDownFakeMongo(test=None):
    """Tear down fake mongo client"""
    # reset test client
    global _testClient
    _testClient = None


# stub mongodb server used for doc tests
def setUpStubMongo(test=None):
    """Setup pymongo client as test client and setup a real empty mongodb"""
    host = 'localhost'
    port = 45017
    tz_aware = True
    sandBoxDir = os.path.join(os.path.dirname(__file__), 'sandbox')
    m01.stub.testing.startMongoDBServer(host, port, sandBoxDir=sandBoxDir)
    # setup pymongo.MongoClient as test client
    global _testClient
    _testClient = pymongo.MongoClient(host, port, tz_aware=tz_aware)
    logger = InstalledHandler('m01.remote')
    test.globs['logger'] = logger
    test.orgJobWorkerArguments = RemoteProcessor.jobWorkerArguments
    test.orgSchedulerWorkerArguments = RemoteProcessor.schedulerWorkerArguments
    RemoteProcessor.jobWorkerArguments = {'waitTime': 0.0}
    RemoteProcessor.schedulerWorkerArguments = {'waitTime': 0.0}
    test.globs['root'] = setUpTestProcessor()


def tearDownStubMongo(test=None):
    """Tear down real mongodb"""
    # stop mongodb server
    sleep = 0.5
    m01.stub.testing.stopMongoDBServer(sleep)
    # reset test client
    global _testClient
    _testClient = None
    logger = test.globs['logger']
    logger.clear()
    logger.uninstall()
    RemoteProcessor.jobWorkerArguments = test.orgJobWorkerArguments
    RemoteProcessor.schedulerWorkerArguments = test.orgSchedulerWorkerArguments
