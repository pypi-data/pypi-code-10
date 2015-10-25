import unittest
from picloud_client import PiCloud


class PiCloudTestCase(unittest.TestCase):

    def setUp(self):
        super(PiCloudTestCase, self).setUp()

    def test_publish_subscribe(self):
        subscriber = PiCloud()

        def on_event(data):
            self.assertEqual(data, 'test')

        subscriber.subscribe(event='whatever', callback=on_event)

        publisher = PiCloud()
        publisher.publish(event='whatever', data='test')

        subscriber.process_subscriptions()
