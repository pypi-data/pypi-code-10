# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import Template, Context
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.test.client import RequestFactory
from django.conf import settings

import django
if django.get_version().startswith("1.4"):
    from django.contrib.auth.models import User
else:
    from django.contrib.auth import get_user_model


class ReamazeTagTest(TestCase):

    TEMPLATE = Template("{% load reamaze %} {% add_reamaze_script %}")

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/dummyview')
        self.request.session = {}

    def test_reamaze_anonymous_not_display(self):
        settings.REAMAZE_OK_FOR_ANONYMOUS = False
        self.request.user = AnonymousUser()
        rendered = self.TEMPLATE.render(Context({'request': self.request,
                                                 'totoa': 'TRTR'}))
        self.assertNotIn("reamaze.js", rendered)

    def test_reamaze_anonymous_display(self):
        settings.REAMAZE_OK_FOR_ANONYMOUS = True
        self.request.user = AnonymousUser()
        self.request.META['HTTP_USER_AGENT'] = 'Firefox'
        self.request.META['HTTP_REFERER'] = 'http_referer'
        rendered = self.TEMPLATE.render(Context({'request': self.request}))
        self.assertIn("reamaze.js", rendered)
        self.assertNotIn("authkey", rendered)

    def test_reamaze_user_display(self):
        if django.get_version().startswith("1.4"):
            self.user = User.objects.create(username='realuser',
                                            email='email@email.com')
        else:
            self.user = get_user_model().objects.create(username='realuser',
                                            email='email@email.com')

        self.request.user = self.user
        self.request.META['HTTP_USER_AGENT'] = 'Firefox'
        self.request.META['HTTP_REFERER'] = 'http_referer'
        rendered = self.TEMPLATE.render(Context({'request': self.request}))
        self.assertIn("reamaze.js", rendered)
        self.assertIn("authkey", rendered)
        self.assertIn("_support['name'] = 'realuser';", rendered)

    def test_reamaze_user_agent_and_no_referer(self):
        if django.get_version().startswith("1.4"):
            self.user = User.objects.create(username='realuser',
                                            email='email@email.com')
        else:
            self.user = get_user_model().objects.create(username='realuser',
                                            email='email@email.com')
        self.request.user = self.user
        self.request.META['HTTP_USER_AGENT'] = 'Firefox'
        rendered = self.TEMPLATE.render(Context({'request': self.request}))
        self.assertIn("reamaze.js", rendered)
        self.assertIn("authkey", rendered)
        self.assertIn("""value: "Firefox""""", rendered)
        self.assertIn("_support['name'] = 'realuser';", rendered)

    def test_reamaze_not_with_channel(self):
        settings.REAMAZE_OK_FOR_ANONYMOUS = True
        settings.REAMAZE_CHANNEL = None
        self.request.user = AnonymousUser()
        self.request.META['HTTP_USER_AGENT'] = 'Firefox'
        self.request.META['HTTP_REFERER'] = 'http_referer'
        rendered = self.TEMPLATE.render(Context({'request': self.request}))
        self.assertIn("reamaze.js", rendered)
        self.assertNotIn("channel", rendered)

    def test_reamaze_with_channel(self):
        settings.REAMAZE_OK_FOR_ANONYMOUS = True
        self.request.user = AnonymousUser()
        self.request.META['HTTP_USER_AGENT'] = 'Firefox'
        self.request.META['HTTP_REFERER'] = 'http_referer'
        rendered = self.TEMPLATE.render(Context({'request': self.request}))
        self.assertIn("reamaze.js", rendered)
        self.assertNotIn("mailbox: 'CHANNEL_NAME'", rendered)
