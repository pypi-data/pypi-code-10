# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve

from rest_framework.test import APITestCase


def from_none(exc):
    """Emulates raise ... from None (PEP 409) on older Python-s
    """
    try:
        exc.__cause__ = None
    except AttributeError:
        exc.__context__ = None
    return exc


class MyMessageTests(APITestCase):
    """
    Messages
    ========

    Group of all messages-related resources.

    My Message
    ----------
    """

    def test_RetrieveaMessage(self):
        """
        Retrieve a Message

        In API Blueprint requests can hold exactly the same kind of information and
        can be described by exactly the same structure as responses, only with
        different signature – using the Request keyword. The string that follows after
        the Request keyword is a request identifier. Again, using an explanatory and
        simple naming is the best way to go.
        """
        url = resolve("/message")
        print("%s.%s: %d requests" % (
            url.func.cls.__module__, url.func.cls.__name__, 2))
        headers = {u'Accept': u'text/plain'}
        response = self.client.get("/message", **headers)
        try:
             self.assertEqual(response.code, 200)
        except AssertionError as e:
             print(response)
             raise from_none(e)
        headers = {u'Accept': u'application/json'}
        response = self.client.get("/message", **headers)
        try:
             self.assertEqual(response.code, 200)
        except AssertionError as e:
             print(response)
             raise from_none(e)

    def test_UpdateaMessage(self):
        """
        Update a Message
        """
        url = resolve("/message")
        print("%s.%s: %d requests" % (
            url.func.cls.__module__, url.func.cls.__name__, 2))
        body = u'All your base are belong to us.'
        response = self.client.put("/message", body, format="plain")
        try:
             self.assertEqual(response.code, 204)
        except AssertionError as e:
             print(response)
             raise from_none(e)
        body = {u'message': u'All your base are belong to us.'}
        response = self.client.put("/message", body, format="json")
        try:
             self.assertEqual(response.code, 204)
        except AssertionError as e:
             print(response)
             raise from_none(e)
