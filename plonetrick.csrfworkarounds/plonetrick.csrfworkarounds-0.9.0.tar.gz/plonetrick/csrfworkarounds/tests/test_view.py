# -*- coding: utf-8 -*-
'''Setup/installation tests for this package.'''

from plonetrick.csrfworkarounds.testing import IntegrationTestCase


class TestInstall(IntegrationTestCase):
    '''Test installation of plonetrick.csrfworkarounds into Plone.'''

    def setUp(self):
        '''Custom shared utility setup for tests.'''
        self.portal = self.layer['portal']
