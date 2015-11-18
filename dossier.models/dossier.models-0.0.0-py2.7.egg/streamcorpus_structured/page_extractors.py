#!/usr/bin/python
# -*- coding: utf-8 -*-
'''Profiles appear in many systems.  A Diffeo system's MediaWiki is
just one source.  The extractors in this module recognize the *slot
values* in an external profile, extract them, and organize them into
an infobox-like data structure that connects string-typed slot names
to lists of Unicode character string values.

.. block-quote:: json

   {slot_name_1: [slot_value_1, ...]}

For example, a slot named "ICQ" can have values such as u"27313331",
and a slot named "phone" can have values such as u"+84-291211111", and
"NAME": u"Andromeda Fo\u0d31baz".  In the future, we might want slots
that have multiple value types, such as "hometown" might have bother
string-type values and coordinate-type values.  For now, many cases
are covered by string-type values to named slots.

The slot values come from two sources at the moment: other selector
extractors that have been run on the body content, and the URL string
of the document.


.. Your use of this software is governed by your license agreement.
   Unpublished Work Copyright 2015 Diffeo, Inc.

'''
from __future__ import absolute_import, division, print_function
#import abc
import cbor
from collections import defaultdict
import logging
from urlparse import urlparse

import regex as re

from dossier.streamcorpus_structured.constants import CANONICAL
from dossier.streamcorpus_structured.cyber_extractors import phonenumber_matcher, \
    email_matcher
from dossier.streamcorpus_structured.utils import extract_field_from_html, \
    extract_field_from_html_si, extract_name_from_url, \
    extract_name_from_title

logger = logging.getLogger(__name__)


class ProfileExtractor(object):
    ## don't actually use abc, because issubclass has issues with
    ## caching weak references
    #__metaclass__ = abc.ABCMeta

    def __init__(self, config=None):
        self.config = config

    def process(self, si, url_parts):
        slots = self.extract_slots(si, url_parts)
        if slots:
            return {'source_name': self.source_name,
                    'slots': slots}
        else:
            return None

    #@abc.abstractmethod
    def extract_slots(self, si, url_parts):
        raise NotImplementedError


class com_vk(ProfileExtractor):

    source_name = 'VK.com'

    def extract_slots(self, si, url_parts):
        slots = {}
        username = extract_name_from_url(url_parts, 0)
        if username:
            slots['username'] = [username]

        NAME = extract_name_from_title(si, '|')
        if NAME:
            slots['NAME'] = [NAME]
        return slots


class com_icq(ProfileExtractor):

    source_name = 'ICQ.com'

    def extract_slots(self, si, url_parts):
        slots = {}
        if not extract_name_from_url(url_parts, 0) == 'people':
            # ignore non-profile pages in icq.com
            return None
        ICQ = extract_name_from_url(url_parts, 1)
        if ICQ:
            slots['ICQ'] = [ICQ]
        else: # if no ICQ string, then probably all wrong
            return None 
        # username is called "nick_name" and is repeated at
        ## <p class="people_user__about" data-user-profile="other_profile_nick_name">

        username = extract_name_from_title(si, '-')
        if username:
            slots['username'] = [username]

        # get it from the raw data
        first_name = extract_field_from_html_si(
            si, '''<span data-user-profile="other_profile_first_name">''', '</span>')
        last_name = extract_field_from_html_si(
            si, '''<span data-user-profile="other_profile_last_name">''', '</span>')
        NAME = u''
        if first_name:
            NAME += first_name
        if last_name and last_name != NAME:
            NAME += last_name
        if NAME:
            if 'NAME' not in slots: slots['NAME'] = set()
            slots['NAME'].add(NAME)

        if 'NAME' in slots:
            if len(slots['NAME']) == 0: 
                slots.pop('NAME')
            else:
                slots['NAME'] = sorted(slots['NAME'])
        if slots: return slots



class ru_galli(ProfileExtractor):

    source_name = 'galli.ru'

    def extract_slots(self, si, url_parts):
        #http://mms.galli.ru/nz?rid=35&anket_id=113032

        slots = {}
        if not 'anket_id' in url_parts.query:
            return None
        for _, selectors in si.body.selectors.items():
            for sel in selectors:
                if sel.selector_type in set(['ICQ', 'SKYPE', 'email', 'PHONE']):
                    if sel.selector_type not in slots:
                        slots[sel.selector_type] = []
                    slots[sel.selector_type].append(sel.canonical_selector)

        if slots: return slots



class ru_ngs(ProfileExtractor):

    source_name = 'ngs.ru'

    def extract_slots(self, si, url_parts):
        # http://realty.ngs.ru/forum/profile/1420647/
        #http://mms.galli.ru/nz?rid=35&anket_id=113032
        #http://forum.ngs.ru/profile/1420647/

        slots = {}
        if not (extract_name_from_url(url_parts, 0) == 'profile' or
                (extract_name_from_url(url_parts, 0) == 'forum' and 
                 extract_name_from_url(url_parts, 1) == 'profile')
                ):
            # ignore non-profile pages in *.ngs.ru
            return None



tags = '''(\s*\<[^>]*\>\s*)*\s*'''
com_tradekey_re = re.compile(
ur'''\<div class="contact-info"\>\s*\<ul\>\s*\<li[^>]*\>\s*'''
ur'''(\<span\>Contact Person[^<]*\</span\>\s*\<a[^>]*\>((Mr|Ms|Mrs|Dr).)?\s*(?P<contact_name>[^<]+)\</a\>)?\s*'''
ur'''\<font.*?\</font\>\s*''' + tags +
ur'''(Company[^<]*''' + tags + '''(?P<company_name>[^<]+))?''' + tags +
ur'''(Address[^<]*''' + tags + '''(?P<address>[^<]+))?''' + tags +
ur'''(Zip/Postal[^<]*''' + tags + '''(?P<postal_code>[^<]+))?''' + tags +
ur'''(Telephone[^<]*''' + tags + '''(?P<telephone>[^<]+))?''' + tags +
ur'''(Fax[^<]*''' + tags + '''(?P<fax>[^<]+))?''' + tags +
ur'''(Mobile[^<]*''' + tags + '''(?P<mobile>[^<]+))?''' + tags
, flags=re.UNICODE | re.MULTILINE | re.IGNORECASE)

company_word_re = re.compile(ur'(深圳|市鸿|科技|有限|公司|Company|Co|Limited Liability|Ltd|'
                             ur'Corporation|Corp|Inc|Incorporated|LLC|Limited)'
                             ur'(\.|\,)*',
                             flags=re.UNICODE | re.IGNORECASE)
whitespace_re = re.compile(ur'(\s|\n|\p{Z})+', flags=re.UNICODE | re.IGNORECASE)

def strip_company_words(val):
    val = company_word_re.sub(' ', val)
    val = whitespace_re.sub(' ', val).strip()
    return val

class com_tradekey(ProfileExtractor):

    source_name = 'tradekey.com'

    re_mapping = {
        'contact_name': 'NAME',
        'company_name': 'NAME',
        #'address': 'address',
        #'postal_code': 'postal_code',
        'telephone': 'PHONE',
        'fax': 'PHONE',
        'mobile': 'PHONE',
        }

    def extract_slots(self, si, url_parts):
        slots = defaultdict(list)
        if not extract_name_from_url(url_parts, 0) == 'company':
            # ignore non-profile pages in tradekey.com
            return None

        match = com_tradekey_re.search(si.body.raw)
        if match:
            for group_name, feature_name in self.re_mapping.items():
                val = match.group(group_name).strip()
                try:
                    val = val.decode('utf8')
                except: 
                    val = None
                if val:
                    slots[feature_name].append(val)

                    if group_name == 'company_name':
                        striped_name = strip_company_words(val)
                        if striped_name:
                            slots['NAME'].append(striped_name)

            if slots['PHONE']:
                normalized_phones = set()
                for raw_string in slots['PHONE']:
                    if not raw_string.startswith('+'):
                        raw_string = '+' + raw_string
                    for sel in phonenumber_matcher(raw_string):
                        if len(sel[CANONICAL]) > 5:
                            normalized_phones.add(sel[CANONICAL])
                slots['PHONE'] = list(normalized_phones)

        if slots: return dict(slots)


class com_hongkongcompanylist(ProfileExtractor):

    source_name = 'hongkongcompanylist.com'

    def extract_slots(self, si, url_parts):
        slots = defaultdict(list)

        name1 = extract_field_from_html_si(
            si, '''>Company Name: </div><div class="covalue"><h2>''', '</h2>')
        name2 = extract_field_from_html_si(
            si, '''>Company Name(CN): </div><div class="covalue"><h2>''', '</h2>')

        if name1 and name2:
            slots['NAME'].append(name1)
            slots['NAME'].append(name2)

            striped_name = strip_company_words(name1)
            if striped_name:
                slots['NAME'].append(striped_name)

            striped_name = strip_company_words(name2)
            if striped_name:
                slots['NAME'].append(striped_name)


        if slots: return slots

class com_zhiqiye(ProfileExtractor):

    source_name = 'zhiqiye.com'

    def extract_slots(self, si, url_parts):
        slots = defaultdict(list)
        if not extract_name_from_url(url_parts, 0) == 'company':
            # ignore non-profile pages in zhiqiye.com
            return None

        name = extract_field_from_html_si(si, '''<h3>''', '</h3>')
        if name:
            slots['NAME'].append(name) #.decode('utf8'))
            striped_name = strip_company_words(name)
            if striped_name:
                slots['NAME'].append(striped_name)

        email_text = extract_field_from_html_si(si, '''邮箱''', '''</td>''')
        email_matches = list(email_matcher(email_text))
        if email_matches:
            email_match = email_matches[0][CANONICAL]
            slots['email'].append(email_match)

        phone_text = extract_field_from_html_si(si, '''手机''', '''</td>''')
        phone_matches = list(phonenumber_matcher(phone_text, country='CN'))
        if phone_matches:
            phone_match = phone_matches[0][CANONICAL]
            slots['PHONE'].append(phone_match)

        if slots: return dict(slots)



url_matchers = {
    'com': {
        'vk': com_vk,
        'icq': com_icq,
        'tradekey': com_tradekey,
        'hongkongcompanylist': com_hongkongcompanylist,
        'zhiqiye': com_zhiqiye,
        },
    'ru': {
        #'ngs': ru_ngs,
        'galli': ru_galli,
        },
    }

def profile_page(si):
    '''dispatcher that uses the url_matchers domain name tree above to
    lookup a callable function that returns a list of *linked
    selectors*, which this function serializes using cbor.

    '''
    try:
        url_parts = urlparse(si.abs_url)
    except:
        logger.warn('failed url extraction: %r', si.abs_url, exc_info=True)
        return
    hostname = url_parts.netloc
    root = url_matchers
    for part in reversed(hostname.split('.')):
        if part in root:
            root = root[part]
        else:
            # do not find a parser for this site
            return None
        if type(root) == type and issubclass(root, ProfileExtractor):
            config = {} # could get this from yakonfig?
            extractor = root(config)
            slot_info = extractor.process(si, url_parts)
            if slot_info:
                data = cbor.dumps(slot_info)
                # transforms.process_text will put data into
                # Selector(... metadata=data)
                return data
            else:
                return
