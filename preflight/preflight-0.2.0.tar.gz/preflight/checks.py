import datetime
import re
import unittest

import bs4
import requests

import accept_types

from .exceptions import BadConfigException
from .utils import get_max_age, parse_cache_time, parse_rfc2822


class Site(unittest.TestSuite):
    def __init__(self, name, domain, **options):
        super().__init__()
        self.name = name
        self.domain = domain
        self.options = options
        self.checkers = []

    def add_check(self, checker):
        self.checkers.append(checker)


class AttrBucket(object):
    bucket = None

    def fill_bucket(self, options, parent):

        bucket_cls = self.Bucket
        bucket_attrs = set(attr
                           for cls in bucket_cls.mro()
                           for attr in cls.__dict__.keys()
                           if not attr.startswith('_'))

        unknown_keys = set(options.keys()) - bucket_attrs
        if unknown_keys:
            raise BadConfigException('Invalid option(s) for {}: {}'.format(
                type(self).__name__, ','.join(unknown_keys)))

        bucket = {}
        for attr in bucket_attrs:
            if attr in options:
                bucket[attr] = options[attr]
            elif attr in parent:
                bucket[attr] = parent[attr]
            else:
                bucket[attr] = getattr(bucket_cls, attr)

        self.bucket = bucket

    def __getitem__(self, key):
        return self.bucket[key]


class RemoteResource(AttrBucket):

    class Bucket():
        status = 200

    def __init__(self, site, path, options):
        super().__init__()
        self.site = site
        self.path = path
        self.fill_bucket(options, site)

    def __str__(self):
        return self.url

    def __repr__(self):
        return '<{}: {}>'.format(type(self).__name__, self)

    @property
    def url(self):
        domain = self.site.domain
        if domain[-1] == '/':
            domain = domain[:-1]
        return domain + self.path

    def get(self):
        return requests.get(self.url)

    def test_status_code(self, response):
        if response.status_code != int(self['status']):
            self.fail('{} responded with {}, not {}'.format(self, response.status_code, self['status']))


class Asset(RemoteResource, unittest.TestCase):

    class Bucket(RemoteResource.Bucket):
        type = '*/*'
        cache_time = None

    def runTest(self):
        response = self.get()

        self.test_status_code(response)
        self.test_content_type(response)
        self.test_expiry(response)

    def test_content_type(self, response):
        content_type = response.headers['Content-Type'].split(';')[0]
        acceptable_type = accept_types.AcceptableType(self['type'])
        matched = acceptable_type.matches(content_type)
        if not matched:
            self.fail('{} is a {}, not a {}'.format(self, content_type, self['type']))

    def test_expiry(self, response):
        if self['cache_time'] is None:
            return

        cache_time = parse_cache_time(self['cache_time'])

        if 'cache-control' in response.headers:
            max_age = get_max_age(response.headers['cache-control'])
            if max_age is not None:
                if max_age < cache_time.total_seconds():
                    self.fail('{} expires after {} seconds, which is less than the required {}'.format(
                        self, max_age, cache_time.total_seconds()))
                return

        if 'expires' in response.headers:
            expiry_date = parse_rfc2822(response.headers['expires'])

            # Give a 10 minute buffer in case of time differences in the server
            now = datetime.datetime.utcnow()
            expected_expiry = now + cache_time - datetime.timedelta(minutes=10)

            if expiry_date < expected_expiry:
                self.fail('{} expires in {}, which is less than the required {}'.format(
                    self, expiry_date - now, cache_time))
            return

        self.fail('No cache time set for {}'.format(self))


class Page(RemoteResource, unittest.TestCase):

    class Bucket(RemoteResource.Bucket):
        google_analytics = None
        google_tag_manager = None

    def runTest(self):
        response = self.get()

        self.test_status_code(response)
        self.test_google_analytics(response)
        self.test_google_tag_manager(response)

    def test_google_analytics(self, response):
        if self['google_analytics'] is None:
            return

        if not re.match(r'^UA-[\d-]+$', self['google_analytics']):
            self.fail('Invalid Google Analytics UA code: {}'.format(self['google_analytics']))

        html = bs4.BeautifulSoup(response.text, "html.parser")
        for script in html.find_all('script'):
            if self['google_analytics'] in script.get_text():
                break
        else:
            self.fail('{} did not have Google Analytics UA code {}'.format(self, self['google_analytics']))

    def test_google_tag_manager(self, response):
        if self['google_tag_manager'] is None:
            return

        if not re.match(r'^GTM-[\w\d]{6,}$', self['google_tag_manager']):
            self.fail('Invalid Google Tag Manager code: {}'.format(self['google_tag_manager']))

        html = bs4.BeautifulSoup(response.text, "html.parser")
        for script in html.find_all('script'):
            if self['google_tag_manager'] in script.get_text():
                break
        else:
            self.fail('{} did not have Google Tag Manager code {}'.format(self, self['google_tag_manager']))
