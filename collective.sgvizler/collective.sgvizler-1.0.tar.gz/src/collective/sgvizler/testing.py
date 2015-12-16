# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.sgvizler


class CollectiveSgvizlerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.sgvizler)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.sgvizler:default')


COLLECTIVE_SGVIZLER_FIXTURE = CollectiveSgvizlerLayer()


COLLECTIVE_SGVIZLER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_SGVIZLER_FIXTURE,),
    name='CollectiveSgvizlerLayer:IntegrationTesting'
)


COLLECTIVE_SGVIZLER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_SGVIZLER_FIXTURE,),
    name='CollectiveSgvizlerLayer:FunctionalTesting'
)


COLLECTIVE_SGVIZLER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_SGVIZLER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveSgvizlerLayer:AcceptanceTesting'
)
