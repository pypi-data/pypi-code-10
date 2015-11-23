# -*- coding:utf-8 -*-
'''
Created on Nov 14, 2015

@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

import argparse
import logging
import os
import urllib2
import warnings

import caldav
import ics


__version__ = '0.2.2'

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Ical2CalDav(object):
    def __init__(self, ics_url, caldav_url, username=None, password=None,
                 calendar_id=None, purge_calendar=False, delay_purge=True):

        self.ics_url = ics_url
        self.caldav_url = caldav_url
        self.username = username
        self.password = password
        self.calendar_id = calendar_id
        self.purge_calendar = purge_calendar
        self.delay_purge = delay_purge


    def __call__(self):
        vcal = self.get_vcal_content()
    #   vcal = self.get_test_vcal()
        events = self.split_events(vcal)
        self.upload_to_dav(events)


    def get_vcal_content(self):
        if os.path.exists(self.ics_url):
            with open(self.ics_url) as f:
                return f.read()
        else:
            return urllib2.urlopen(self.ics_url).read()


    def split_events(self, vcal):
        c = ics.Calendar(vcal.decode('utf-8'))
        logger.info('Found %s event in %s', len(c.events), self.ics_url)
        return c.events


    def fix_uid(self, uid):
        ''' overwrite this method if you want to change event.uid '''
        pass


    def upload_to_dav(self, events):
        logger.debug('try to connect to dav server')
        client = caldav.DAVClient(url=self.caldav_url, username=self.username, password=self.password, ssl_verify_cert=False)
        logger.debug('getting principal')
        principal = client.principal()
        logger.debug('getting principal.calendars')
        calendars = principal.calendars()

        #--- select calender to work with
        calendar = None
        for cal in calendars:
            cu = cal.canonical_url
            logger.debug('Found %s', cu)
            if self.calendar_id and cu.endswith('/%s/' % self.calendar_id):
                calendar = cal

        if self.calendar_id is None:
            calendar = calendars[0]

        if calendar is None:
            if self.calendar_id:
                logger.error('no calendar found with id `%s`', self.calendar_id)
            else:
                logger.error('no calendar found.')
            return
        logger.info('Using %s', calendar)

        #--- purge calendar if needed
        purge_uids = []
        l = len(calendar.events())
        if self.purge_calendar and l > 0:
            if not self.delay_purge:
                logger.info('Purging calendar %s before importing (%s events)', calendar, l)
            for ev in calendar.events():
                if self.delay_purge:
                    uid = ev.instance.vevent.uid.value
                    purge_uids.append(uid)
                    logger.debug('will purge if not overwrited %s', uid)
                else:
                    logger.debug('purging %s', ev)
                    ev.delete()

        #--- import event to calendar
        for event in events:
            new_uid = self.fix_uid(event.uid)
            if new_uid:
                event.uid = new_uid
            try:
                purge_uids.remove(event.uid)
            except ValueError:
                pass

            ev = ('BEGIN:VCALENDAR\n'
                  'VERSION:2.0\n'
                  'CALSCALE:GREGORIAN'
                  'PRODID:-ics2caldav.py\n'
                  '%s\n'
                  'END:VCALENDAR'
                  ) % str(event)
        #   print ev, '\n', '=' * 30
            res = calendar.add_event(ev)
            logger.debug('%s created', res)

        #--- now purge them
        for uid in purge_uids:
            ev = calendar.event_by_uid(uid)
            logger.debug('purging %s', ev)
            ev.delete()

        logger.info('done.')


    def get_test_vcal(self):
        return '\n'.join((
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-ics2caldav.py',
            'BEGIN:VEVENT',
            'UID:1234567890',
            'CREATED;VALUE=DATE:20120702Z',
            'DTSTAMP:20151114T182145Z',
            'DTSTART:20151114T170000Z',
            'DTEND:20151114T180000Z',
            'SUMMARY:First Test',
            'END:VEVENT',
            'BEGIN:VEVENT',
            'UID:1234567891',
            'DTSTAMP:20151115T182145Z',
            'DTSTART:20151115T170000Z',
            'DTEND:20151115T180000Z',
            'SUMMARY:Second test event',
            'END:VEVENT',
            'END:VCALENDAR',
        ))


    @classmethod
    def parse_args(cls, args=None):
        parser = argparse.ArgumentParser(description='import events from ics to caldav')

        parser.add_argument('-i', '--ics', metavar='url', type=str, action='store', required=True, help='url to ics calendar which want to get events from')
        parser.add_argument('-c', '--caldav', metavar='url', type=str, action='store', required=True, help='url to CalDAV server which want to put event to')
        parser.add_argument('-d', '--calid', metavar='calendar_id', type=str, action='store', help='CalDAV calendar id')
        parser.add_argument('-u', '--username', metavar='username', type=str, action='store', help='CalDAV username')
        parser.add_argument('-p', '--password', metavar='password', type=str, action='store', help='CalDAV password')
        parser.add_argument('--purge', action='store_true', help='purge calendar')
        parser.add_argument('--delay', action='store_true', help='delay purge calendar')

        args = parser.parse_args(args)

        return cls(
            ics_url=args.ics,
            caldav_url=args.caldav,
            calendar_id=args.calid,
            username=args.username,
            password=args.password,
            purge_calendar=args.purge,
            delay_purge=args.delay,
        )()


    @staticmethod
    def config_logger():
        warnings.simplefilter('ignore')

        hdlr = logging.StreamHandler()
        hdlr.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)
