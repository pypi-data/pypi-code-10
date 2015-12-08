from DateTime import DateTime
from Products.ATContentTypes.interface.interfaces import ICalendarSupport
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class CalendarExportResults(BrowserView):

    template = ViewPageTemplateFile('results.pt')

    def __call__(self):
        props = getToolByName(self.context, 'portal_properties').get(
            'calendarexport_properties', None)
        if not props:
            return
        self.enable_ical = props.getProperty('ical_export')
        self.enable_pdf = props.getProperty('pdf_export')
        
        if self.request.form.get('export-events', '') == 'pdf':
            return getMultiAdapter((self.context, self.request),
                                   name=u'export_pdf')()
        elif self.request.form.get('export-events', '') == 'ical':
            return getMultiAdapter((self.context, self.request),
                                   name=u'export_ics')()
        return self.template()

    def events(self):
        """ Returns events searching 'from' and 'to' from request.
            If there are no data in request returns nothing.
        """
        catalog = getToolByName(self.context, 'portal_catalog')
        if self.request.form.get('from','') and self.request.form.get('to',''):
            start = self.request.form.get('from','').split('.')
            start.reverse()
            start = DateTime(*[int(p) for p in start]).earliestTime()
            end = self.request.form.get('to','').split('.')
            end.reverse()
            end = DateTime(*[int(p) for p in end]).latestTime()
            return catalog(dict(
                object_provides = ICalendarSupport.__identifier__,
                start = {'range':'min', 'query': start},
                end = {'range':'max', 'query': end}))
        return
