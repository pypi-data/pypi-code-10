#!/usr/bin/python
# -*- coding: utf-8 -*-
'''Test cases for page extractors for selector chaining.

.. Your use of this software is governed by your license agreement.
   Unpublished Work Copyright 2015 Diffeo, Inc.

'''

import cbor
import os
import pytest
from streamcorpus import Offset, EntityType, make_stream_item
from dossier.streamcorpus_structured.transform import structured_features
from dossier.streamcorpus_structured.page_extractors import profile_page
from streamcorpus_pipeline._clean_html import clean_html
from streamcorpus_pipeline._clean_visible import clean_visible


examples =    [
        (True, 'data/vk.html', 'https://vk.com/minsk', {'username': [u'minsk'], 'NAME': [u'Alyaxandr Bulbash']}),
        (True, 'data/icq.html', 'https://www.icq.com/people/100001', {'ICQ': [u'100001'], 'NAME': [u"\xa0'\u2020 Raven '\u2020"], 'username': [u"\xa0'\u2020 Raven '\u2020"]}),
        (False, 'data/galli.ru.html', 'http://mms.galli.ru/nz?rid=35&anket_id=113032', {'ICQ': [u'266616226'], 'email': [u"killxp@mail.ru"] }),
        (True, 'data/tradekey.com-Nenets-Oil-Company-7088151.html', 
         'http://www.tradekey.com/company/Reality-Electronics-Co-Limited-4601105.html',
         {'NAME': [u'Maxim Kozlov', u'Nenets Oil', u'Nenets Oil Company'],
          #'address': [u'Arkhangelsk oblast,, Nenets AO, Zapolyarny district, Russia'],
          #'postal_code': [u'166700'],
          'PHONE': [u'+79265036203', u'+79260021370', u'+79265036203']}),
        (True, 'data/tradekey.com-Reality-Electronics-Co-Limited-4601105.html', 
         'http://www.tradekey.com/company/Nenets-Oil-Company-7088151.html',
         {'NAME': [u'Vera Yau', u'Reality Electronics', u'Reality Electronics Co., Limited.'],
          #'address': [u'HouHai, Shenzhen, Guangdong, China'],
          #'postal_code': [u'518067'],
          'PHONE': [u'+8675526881721', u'+8675526881720', u'+8613631630842']}),
        (True, 'data/hongkongcompanylist.com-reality-electronics-co-limited-btfffof.html',
         'http://www.hongkongcompanylist.com/reality-electronics-co-limited-btfffof',
         {'NAME': [u'瑞安電子', u'瑞安電子科技有限公司', 
                   u'Reality Electronics', u'Reality Electronics Co., Limited']}),
        (True, 'data/zhiqiye.com-27C4E2C2A87B4EF982EF4CF9EE0E1665-index.html',
         'http://www.zhiqiye.com/company/27C4E2C2A87B4EF982EF4CF9EE0E1665/index.html',
         {'NAME': [u'瑞安电子', u'深圳市鸿瑞安电子科技有限公司'],
          'PHONE': [u'+8613129595815'],
          'email': [u'hra1212@163.com'],
      }),
]

def set_wrap(d):
    return {k: set(v) for k, v in d.items()}

@pytest.mark.parametrize('simple,path,url,expected_slot_data', examples)
def test_profile_page(simple, path, url, expected_slot_data):
    if not simple: return
    si = make_stream_item(0, url)
    path = os.path.join(os.path.dirname(__file__), path)
    si.body.raw = open(path).read()
    results = profile_page(si)
    assert results
    data = cbor.loads(results)
    assert set_wrap(data['slots']) == set_wrap(expected_slot_data)


@pytest.yield_fixture
def gali_page_example():
    simple, path, url, expected_slot_data = examples[2]
    si = make_stream_item(0, url)
    path = os.path.join(os.path.dirname(__file__), path)
    si.body.raw = open(path).read()

    ch = clean_html({})
    cv = clean_visible({})
    xform = structured_features({'tagger_id_to_create': 'foo'})

    si = ch(si, {})
    si = cv(si, {})
    si = xform(si)

    yield si, expected_slot_data


@pytest.yield_fixture(params=examples)
def profile_page_examples(request):
    simple, path, url, expected_slot_data = request.param
    si = make_stream_item(0, url)
    path = os.path.join(os.path.dirname(__file__), path)
    si.body.raw = open(path).read()

    ch = clean_html({})
    cv = clean_visible({})
    xform = structured_features({'tagger_id_to_create': 'foo'})

    si = ch(si, {})
    si = cv(si, {})
    si = xform(si)

    yield si, expected_slot_data


def test_profile_page_examples(profile_page_examples):

    si, expected_slot_data = profile_page_examples
    assert si.body.selectors['foo']
    for selector in  si.body.selectors['foo']:
        if selector.selector_type == 'PROFILE_PAGE':
            data = cbor.loads(selector.metadata)
            assert set_wrap(data['slots']) == set_wrap(expected_slot_data)
            break
