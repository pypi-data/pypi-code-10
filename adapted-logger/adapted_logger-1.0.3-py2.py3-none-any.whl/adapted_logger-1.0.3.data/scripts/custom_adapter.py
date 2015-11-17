#__author__ = 'ismailkaboubi'


import logging


class CustomAdapter(logging.LoggerAdapter):
    """
    This  adapter expects the passed in dict-like object to have a
    'ip' key, whose value in brackets is prepended to the log message.
    """
    def process(self, msg, kwargs):
        return '%s    %s' % (self.extra['ip'], msg), kwargs
