import os
import unittest
from picloud_client import SubClient, PubClient


class PiCloudTestCase(unittest.TestCase):

    def setUp(self):
        super(PiCloudTestCase, self).setUp()

    def test_publish_subscribe(self):
        picloud_sub_url = os.getenv('PICLOUD_SUB_URL')
        picloud_pub_url = os.getenv('PICLOUD_PUB_URL')
        picloud_api_key = os.getenv('PICLOUD_API_KEY')

        subscriber = SubClient(
            url=picloud_sub_url,
            api_key=picloud_api_key,
            client_name='Test-Client')

        def on_event(data):
            self.assertEqual(data, 'test')

        subscriber.subscribe(event='whatever', callback=on_event)

        publisher = PubClient(
            url=picloud_pub_url,
            api_key=picloud_api_key,
            client_name='Test-Client')
        publisher.publish(event='whatever', data='test')

        subscriber.process_subscriptions()
