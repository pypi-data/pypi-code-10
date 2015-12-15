import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import uwosh.default

from zope.app import zapi
from zope.configuration import xmlconfig


ztc.installProduct('uwosh.default')
ztc.installProduct('uwosh.requirements')
ptc.setupPloneSite(products=('uwosh.default', 'uwosh.requirements'))


class UWOshDefaultTestCase(ptc.PloneTestCase):
    """
    """