# -*- coding: utf-8 -*-
'''
Pagerduty actions
'''
from __future__ import absolute_import

import pygerduty
import logging

from pagerduty import broker

logger = logging.getLogger(__name__)


class IncidentKeyLocked(Exception):
    '''
    Exception for when the incident key has already been used recently
    '''
    pass


class IncidentKeyLock(object):
    '''
    Check for if an incident was already used
    '''
    _rconn = None

    def __init__(self, incident_key, settings):
        '''
        Args:
            incident_key (str): unique incident key to tie to error
            settings (object): settings object
        Returns:
            None
        '''
        self.incident_key = incident_key
        self.settings = settings

    @property
    def rconn(self):
        '''
        Redis connection object
        '''
        if self._rconn is None:
            logger.info(broker)
            self._rconn = broker.RedisClass(self.settings)
        return self._rconn

    def __enter__(self):
        '''
        Create a lock on redis to decrease the number of alerts to the pagerduty api
        '''
        logger.info('Check for redis lock: {0}'.format(self.incident_key))

        # First check for a redis lock
        rlock_status = self.rconn.set(self.incident_key, 'locked', ex=180, nx=True)
        if rlock_status is None:
            logger.info('Redis lock already exists for incident: {0}.'.format(self.incident_key))
            raise IncidentKeyLocked("IncidentKey {0} is locked via Redis".format(self.incident_key), None)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        Only clean up the lock if the alert failed.
        This should be left to expire if there is not an error, to help keep extra
        calls from going through for 180 seconds.  To decrease the amount of time
        we spend alerting pagerduty.
        '''
        if exc_type is not None:
            self.rconn.delete(self.incident_key)


class Pager(object):
    pager = None
    settings = None

    def __new__(cls, settings):
        '''
        Cache base class
        Args:
            settings (object): pagerduty settings
        Returns:
            Pager (object): trigger incidents on pagerduty api
        '''
        if cls.pager is None:
            cls.settings = settings
            # api_token is not actually used for what we are doing, we don't
            # need to auth only send to the service_key below
            cls.pager = pygerduty.PagerDuty(cls.settings.PAGERDUTY_SUBDOMAIN, api_token='junk')
        return super(Pager, cls).__new__(cls)

    def trigger_incident(self, description, incident_key, details=None, client=None, client_url=None):
        '''
        Trigger an incident in the pagerduty api
        Args:
            description (str): Description on why alert is called
            incident_key (str): unique string for incident
            details (dict): dictionary with extra details
            client (str): arbitrary product name
            client_url (str): arbitrary product url
        Returns:
            bool:
                True if the call succeeded
                False if the call failed
                None if no call was made
        '''
        if self.settings.PAGERDUTY_SERVICE_KEY is None:
            return None
        service_key = self.settings.PAGERDUTY_SERVICE_KEY
        try:
            with IncidentKeyLock(incident_key, self.settings):
                self.pager.trigger_incident(service_key, description, "trigger",
                                            details, incident_key,
                                            client=client, client_url=client_url)
            return True
        except IncidentKeyLocked:
            return None
