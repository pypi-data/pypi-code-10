# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.sgvizler.testing import COLLECTIVE_SGVIZLER_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.sgvizler is properly installed."""

    layer = COLLECTIVE_SGVIZLER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.sgvizler is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('collective.sgvizler'))

    def test_browserlayer(self):
        """Test that ICollectiveSgvizlerLayer is registered."""
        from collective.sgvizler.interfaces import ICollectiveSgvizlerLayer
        from plone.browserlayer import utils
        self.assertIn(ICollectiveSgvizlerLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_SGVIZLER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.sgvizler'])

    def test_product_uninstalled(self):
        """Test if collective.sgvizler is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('collective.sgvizler'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveSgvizlerLayer is removed."""
        from collective.sgvizler.interfaces import ICollectiveSgvizlerLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveSgvizlerLayer, utils.registered_layers())
