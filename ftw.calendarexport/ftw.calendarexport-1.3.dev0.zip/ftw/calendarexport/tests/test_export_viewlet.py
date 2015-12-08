from unittest2 import TestCase
from ftw.calendarexport.testing import FTW_CALENDAREXPORT_INTEGRATION_TESTING
from ftw.builder import create
from ftw.builder import Builder
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
import transaction
from ftw.testbrowser import browsing

class TestCalendarExport(TestCase):
    
    layer = FTW_CALENDAREXPORT_INTEGRATION_TESTING
    
    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        transaction.commit()

    @browsing
    def test_export_viewlet(self, browser):
        folder = create(Builder('folder').titled('testfolder'))
        event1 = create(Builder('event').titled(
            'event1').within(
            folder).having(
            startDate='2014-01-23 11:00', endDate='2014-01-23 13:00'))
        event2 = create(Builder('event').titled(
        'event2').within(
        folder).having(
        startDate='2014-01-25 11:00', endDate='2014-01-25 13:00'))
        transaction.commit()
        browser.login().visit(folder, view='ftwcalendar_view')
        self.assertTrue(browser.css('#calexport').text)
        