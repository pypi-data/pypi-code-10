from unittest2 import TestCase
from ftw.calendarexport.testing import FTW_CALENDAREXPORT_INTEGRATION_TESTING
from ftw.builder import create
from ftw.builder import Builder
from plone.app.testing import setRoles
from plone.app.testing import login
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

class TestCalendarExport(TestCase):
    
    layer = FTW_CALENDAREXPORT_INTEGRATION_TESTING
    
    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        
    def test_export(self):
        folder = create(Builder('folder').titled('testfolder'))
        event1 = create(Builder('event').titled(
            'event1').within(
            folder).having(
            startDate='2014-01-23 11:00', endDate='2014-01-23 13:00'))
        event2 = create(Builder('event').titled(
        'event2').within(
        folder).having(
        startDate='2014-01-25 11:00', endDate='2014-01-25 13:00'))
        view = folder.restrictedTraverse('export_ics')
        uids = []
        uids.append(event1.UID())
        uids.append(event2.UID())
        self.portal.REQUEST.form['uids'] = uids
        view()
        feeddata = view.feeddata()
        feed_list = feeddata.split('BEGIN:VEVENT')
        self.assertIn('SUMMARY:event1\nDTSTART:20140123T100000Z\n'
        'DTEND:20140123T120000Z\nCLASS:PUBLIC\nEND:VEVENT\n', feed_list[1])
        self.assertIn('SUMMARY:event2\nDTSTART:20140125T100000Z\n'
        'DTEND:20140125T120000Z\nCLASS:PUBLIC\nEND:VEVENT\nEND:VCALENDAR\n',
            feed_list[2])
        
