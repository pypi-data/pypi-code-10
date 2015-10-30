import urllib
from operator import itemgetter
try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from ProfileContainer import profile_container
import ProfilerPatch

"""Here the actual patching of the expression calls takes place

Of course this is also used to register the product code to Zope
"""

"""
Copyright (c) 2003 Infrae. All rights reserved.
See also LICENSE.txt
Version of this file: $Revision: 1.11 $
Written by Guido Wesdorp
E-mail: guido@infrae.com
"""


class PTProfilerViewer(SimpleItem):
    """The view object for the PTProfiler
    """

    security = ClassSecurityInfo()
    meta_type = 'PTProfiler Viewer'

    manage_options = (
        {'label': 'View', 'action': 'view_tab'},
    ) + SimpleItem.manage_options

    manage_main = view_tab = PageTemplateFile(
        'www/PTProfilerViewTab', globals(), __name__='view_tab')

    _perm = 'View PTProfiler'

    def __init__(self, id, title):
        self.id = id
        self.title = title

    security.declareProtected(_perm, 'full_result')
    def full_result(self, name=None):
        res = profile_container._templates

        if name:
            return res[name]
        else:
            return res

    security.declareProtected(_perm, 'result_sorted_by_time')
    def result_sorted_by_time(self, name):
        """Returns a list of (expr, time, hits) tuples sorted by time"""
        res = profile_container._templates[name]

        ret = []
        for expr, value in res.items():
            if not expr == 'total':
                ret.append((expr, value['time'], value['hits']))

        ret.sort(self._sort_by_time)

        return ret

    security.declareProtected(_perm, 'profiled_templates_full')
    def profiled_templates_full(self):
        sortby = self.REQUEST.get('sortby', None)
        result = []
        for tmpl, info in profile_container._templates.items():
            total = info.get('total', None)
            if total is None:
                time = 'Running'
                hits = 'Running'
                per_hit = 'Running'
            else:
                time = round(total['time'], 4)
                hits = total['hits']
                per_hit = round(time / hits, 4)

            result.append(dict(
                id=tmpl,
                time=time,
                hits=hits,
                per_hit=per_hit,
            ))
        if sortby:
            result = sorted(result, key=itemgetter(sortby), reverse=True)
        return result

    security.declareProtected(_perm, 'total_rendering_time')
    def total_rendering_time(self, ptname):
        return profile_container._templates[ptname]['total']['time']

    security.declareProtected(_perm, 'total_pt_hits')
    def total_pt_hits(self, ptname):
        return profile_container._templates[ptname]['total']['hits']

    security.declareProtected(_perm, 'total_expression_time')
    def total_expression_time(self, ptname):
        total = 0.0
        for key, value in profile_container._templates[ptname].items():
            if not key == 'total':
                total += value['time']
        return total

    security.declareProtected(_perm, 'total_expression_hits')
    def total_expression_hits(self, ptname):
        total = 0
        for key, value in profile_container._templates[ptname].items():
            if not key == 'total':
                total += value['hits']
        return total

    security.declareProtected(_perm, 'clear')
    def clear(self):
        profile_container.clear()

    security.declareProtected(_perm, 'enable')
    def enable(self):
        ProfilerPatch.enabled = 1

    security.declareProtected(_perm, 'disable')
    def disable(self):
        ProfilerPatch.enabled = 0

    security.declareProtected(_perm, 'enabled')
    def enabled(self):
        return ProfilerPatch.enabled

    def _sort_by_time(self, a, b):
        return cmp(b[1], a[1])

InitializeClass(PTProfilerViewer)

manage_addPTProfilerViewerForm = PageTemplateFile(
        'www/addPTProfilerViewer', globals(),
        __name__='manage_addPTProfilerViewerForm')


def manage_addPTProfilerViewer(self, id, title='', REQUEST=None):
    """Add viewer
    """
    id = self._setObject(id, PTProfilerViewer(id, title))
    if REQUEST is None:
        return ''
    try:
        u = self.DestinationURL()
    except:
        u = REQUEST['URL1']
    if REQUEST.has_key('submit_edit'):
        u = '%s/%s' % (u, urllib.quote(id))
    REQUEST.RESPONSE.redirect(u + '/manage_main')
    return ''
