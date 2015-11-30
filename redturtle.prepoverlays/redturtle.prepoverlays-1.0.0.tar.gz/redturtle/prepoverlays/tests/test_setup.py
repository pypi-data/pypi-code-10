# -*- coding: utf-8 -*-
'''Setup/installation tests for this package.'''
from Products.CMFCore.utils import getToolByName
from redturtle.prepoverlays.testing import IntegrationTestCase


class TestInstall(IntegrationTestCase):
    '''Test installation of redturtle.prepoverlays into Plone.'''

    def setUp(self):
        '''Custom shared utility setup for tests.'''
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.jsregistry = getToolByName(self.portal, 'portal_javascripts')

    def test_product_installed(self):
        '''Test if redturtle.prepoverlays is installed with
        portal_quickinstaller.
        '''
        self.assertTrue(
            self.installer.isProductInstalled('redturtle.prepoverlays')
        )

    def test_uninstall(self):
        '''Test if redturtle.prepoverlays is cleanly uninstalled.'''
        self.installer.uninstallProducts(['redturtle.prepoverlays'])
        self.assertFalse(
            self.installer.isProductInstalled('redturtle.prepoverlays')
        )

    def test_browserlayer(self):
        '''Test that IRedturtlePrepoverlaysLayer is registered.'''
        from redturtle.prepoverlays.interfaces import (
            IRedturtlePrepoverlaysLayer
        )
        from plone.browserlayer import utils
        self.failUnless(
            IRedturtlePrepoverlaysLayer in utils.registered_layers()
        )

    def test_jsregistry(self):
        '''Test that jsregistry.xml is parsed'''
        js_ids = (
            '++resource++redturtle.prepoverlays/overlays.js',
        )
        for js_id in js_ids:
            self.assertNotEqual(self.jsregistry.getResource(js_id), None)
