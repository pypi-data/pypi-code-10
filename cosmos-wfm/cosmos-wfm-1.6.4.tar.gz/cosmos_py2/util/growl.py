from __future__ import absolute_import
import sys


def send(message, hostname=None, sticky=True):
    try:
        from gntp import notifier
        import os

        if hostname == None:
            hostname = os.environ.get(u'SSH_CONNECTION', u'localhost').split(u' ')[0]
        growl = notifier.GrowlNotifier(
            applicationName=u"Cosmos",
            notifications=[u"New Updates", u"New Messages"],
            defaultNotifications=[u"New Messages"],
            hostname=hostname,
        )
        growl.register()

        # Send one message
        growl.notify(
            noteType=u"New Messages",
            title=u"Cosmos",
            description=message,
            sticky=sticky,
            priority=1,
        )
    except Exception, e:
        print >>sys.stderr, u'*** ERROR sending growl notification to %s: %s' % (hostname, e)