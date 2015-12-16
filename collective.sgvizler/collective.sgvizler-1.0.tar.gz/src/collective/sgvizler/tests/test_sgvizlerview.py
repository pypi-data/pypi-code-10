# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from collective.sgvizler.testing import COLLECTIVE_SGVIZLER_INTEGRATION_TESTING  # noqa
from collective.sgvizler.interfaces import ISGVizlerView

import unittest2 as unittest


class SGVizlerViewIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_SGVIZLER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='SGVizlerView')
        schema = fti.lookupSchema()
        self.assertEqual(ISGVizlerView, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='SGVizlerView')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='SGVizlerView')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(ISGVizlerView.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('SGVizlerView', 'SGVizlerView')
        self.assertTrue(
            ISGVizlerView.providedBy(self.portal['SGVizlerView'])
        )
