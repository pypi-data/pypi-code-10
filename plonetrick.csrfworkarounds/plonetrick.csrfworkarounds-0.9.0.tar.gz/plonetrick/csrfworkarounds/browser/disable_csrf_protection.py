# coding=utf-8
from Products.Five import BrowserView
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class View(BrowserView):

    def disable(self):
        ''' Disable CSRF protection for this request
        '''
        alsoProvides(
            self.request,
            IDisableCSRFProtection,
        )

    def __call__(self):
        return "Disabled protection for %r" % self.request
