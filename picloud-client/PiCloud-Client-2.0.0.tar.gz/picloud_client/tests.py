import unittest
from picloud_client import PiCloud


class PiCloudTestCase(unittest.TestCase):

    def setUp(self):
        super(PiCloudTestCase, self).setUp()

    def test_publish_subscribe(self):
        subscriber = PiCloud(client_name='Test')

        def on_event(data):
            self.assertEqual(data, 'test')

        subscriber.subscribe(event='whatever', callback=on_event)

        publisher = PiCloud(client_name='Test')
        publisher.publish(event='whatever', data='test')

        subscriber.process_subscriptions()
