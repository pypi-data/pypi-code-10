import unittest

from pushalot.factory import PushalotFactory
from pushalot.apis import APILatest
from pushalot.transport import HTTPTransport

class DummyAPI(object):
    pass

class DummyTransport(object):
    pass

class FactoryTests(unittest.TestCase):

    def test_without_token_raises_exception(self):
        with self.assertRaises(TypeError):
            pushalot = PushalotFactory.create()

    def test_with_token_success(self):
        pushalot = PushalotFactory.create(token='some-token')

    def test_invalid_api_raises_exception(self):
        with self.assertRaises(RuntimeError):
            pushalot = PushalotFactory.create(
                token='some-token',
                api=DummyAPI
            )

    def test_valid_api_used_success(self):
        pushalot = PushalotFactory.create(
            token='some-token',
            api=APILatest
        )

    def test_factory_initiates_correct_default_api(self):
        pushalot = PushalotFactory.create(
            token='some-token',
        )
        self.assertEqual(pushalot.__class__.__name__, 'APILatest')

    def test_invalid_transport_raises(self):
        with self.assertRaises(RuntimeError):
            pushalot = PushalotFactory.create(
                token='some-token',
                transport=DummyTransport
            )

    def test_valid_transport_success(self):
        pushalot = PushalotFactory.create(
            token='some-token',
            transport=HTTPTransport
        )

    def test_factory_uses_correct_default_transport(self):
        pushalot = PushalotFactory.create(
            token='some-token',
        )
        self.assertEqual(pushalot._transport.__class__.__name__, 'HTTPTransport')

