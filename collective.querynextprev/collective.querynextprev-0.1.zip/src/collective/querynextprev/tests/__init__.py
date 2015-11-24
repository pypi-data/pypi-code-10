# -*- coding: utf-8 -*-
import json


query = json.dumps({
    'portal_type': 'Document',
    'sort_on': 'sortable_title'
    })


class DummyView(object):
    pass
