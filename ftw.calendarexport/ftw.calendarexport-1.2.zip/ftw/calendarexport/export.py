from Products.ATContentTypes.interface.interfaces import ICalendarSupport
from plone.memoize import ram
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.lib import calendarsupport as cs
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from Acquisition import aq_inner
from Products.ATContentTypes.browser.calendar import CalendarView, cachekey


class ExportEvents(ViewletBase):
    render = ViewPageTemplateFile('export.pt')

    def active(self):
        props = getToolByName(self.context, 'portal_properties').get(
            'calendarexport_properties', None)
        if not props:
            return False
        return props.getProperty('active')


class ExportICS(CalendarView):

    def update(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        provides = ICalendarSupport.__identifier__
        uids = self.request.form.get('uids', [])
        self.events = catalog(UID=uids, object_provides=provides)
        if not uids:
            self.events = []

    @ram.cache(cachekey)
    def feeddata(self):
        data = cs.ICS_HEADER % dict(prodid=cs.PRODID)
        for brain in self.events:
            tmp_data = brain.getObject().getICal()
            data += tmp_data
        data += cs.ICS_FOOTER
        return data
