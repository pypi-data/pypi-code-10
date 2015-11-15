# -*- coding:utf-8 -*-
'''
Created on Nov 14, 2015

@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

import io

from caldav.lib import vcal
from caldav.lib.python_utilities import to_unicode
from caldav.objects import CalendarObjectResource
from ics.component import Extractor
from ics.event import Event
import vobject


def patch_module_caldav():
    # patch CalendarObjectResource not to raise error

    def _new_set_data(self, data):
        self._data = vcal.fix(data)
        self._instance = vobject.readOne(io.StringIO(to_unicode(self._data)), transform=False)
        return self

    CalendarObjectResource._set_data = _new_set_data
    CalendarObjectResource.data = property(
                                           CalendarObjectResource._get_data,
                                           CalendarObjectResource._set_data,
                                           doc="vCal representation of the object")
    #
    print('patch caldav done.')


def patch_module_ics():
    # patch ics py not to change DTSTART, DTEND

    def new_start(func):
        def start(event, line):
            func(event, line)
            if line:
                event.begin_line = line
        return start

    def o_start(event, container):
        if event.begin:
            container.append(event.begin_line)

    def new_end(func):
        def end(event, line):
            func(event, line)
            if line:
                event.end_line = line
        return end

    def o_end(event, container):
        if event.end:
            container.append(event.end_line)

    #---
    for i, ex in enumerate(Event._EXTRACTORS):
        if ex.type == 'DTSTART':
            Event._EXTRACTORS[i] = Extractor(new_start(ex.function),
                                             ex.type, ex.required, ex.multiple)

        if ex.type == 'DTEND':
            Event._EXTRACTORS[i] = Extractor(new_end(ex.function),
                                             ex.type, ex.required, ex.multiple)

    for i, o in enumerate(Event._OUTPUTS):
        if o.__name__ == 'o_start':
            Event._OUTPUTS[i] = o_start

        if o.__name__ == 'o_end':
            Event._OUTPUTS[i] = o_end

    print('patch ics py done.')



