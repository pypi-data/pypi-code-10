# -*- coding: utf-8 -*-
'''Base module for unittesting.'''

from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2

import unittest2 as unittest


class PlonetrickCsrfworkaroundsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        '''Set up Zope.'''
        # Load ZCML
        import plonetrick.csrfworkarounds
        self.loadZCML(package=plonetrick.csrfworkarounds)
        z2.installProduct(app, 'plonetrick.csrfworkarounds')

    def setUpPloneSite(self, portal):
        '''Set up Plone.'''
        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

    def tearDownZope(self, app):
        '''Tear down Zope.'''


FIXTURE = PlonetrickCsrfworkaroundsLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="PlonetrickCsrfworkaroundsLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="PlonetrickCsrfworkaroundsLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    '''Base class for integration tests.'''

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    '''Base class for functional tests.'''

    layer = FUNCTIONAL_TESTING
