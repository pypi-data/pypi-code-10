from Products.PloneTestCase.PloneTestCase import PloneTestCase
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc
from uwosh.default.tests.base import UWOshDefaultTestCase
from zope.configuration.xmlconfig import xmlconfig, XMLConfig
import uwosh.default.tests
from cStringIO import StringIO
import zope.app.publisher.browser
from Products.Five.testbrowser import Browser
from uwosh.core.utils import *

class TestUtils(UWOshDefaultTestCase):
    """
    Not sure how to test because an actual server never gets started up
    and urllib can't can data that way...
    """

    def afterSetUp(self):
        self.setRoles(('Manager',))
        
    def test_one_of_these_is_in_is_true(self):
        
        x = [1,2,3,4]
        y = [3,4,5,6]
        z = [9,10,11]
        self.failUnless(one_of_these(x).is_in(y), True)
        
    def test_one_of_these_is_in_is_false(self):
        x = [1,2,3,4]
        y = [3,4,5,6]
        z = [9,10,11]
        self.failUnless(one_of_these(x).is_in(z), False)
        
    def test_each_one_of_these_is_in(self):
        x = [1,2,3]
        y = [1,2,3,4,5]
        self.failUnless(each_one_of_these(x).is_in(y))
        
    def test_each_one_of_these_is_in_failure(self):
        x = [1,2,3,7]
        y = [1,2,3,4,5]
        self.failUnless(not each_one_of_these(x).is_in(y))
        
    def test_each_one_of_these_is_not_in(self):
        x = [1,2,3]
        y = [4,5,6]
        self.failUnless(each_one_of_these(x).is_not_in(y))
        
    def test_each_one_of_these_is_not_in_failure(self):
        x = [1,2,3,4]
        y = [4,5,6]
        self.failUnless(not each_one_of_these(x).is_not_in(y))
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestRemoteService))
    
    return suite