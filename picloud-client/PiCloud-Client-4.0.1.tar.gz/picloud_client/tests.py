import os
import unittest
from picloud_client import SocketClient, HttpClient


class PiCloudTestCase(unittest.TestCase):

    def setUp(self):
        super(PiCloudTestCase, self).setUp()

    def test_publish_subscribe(self):
        picloud_socket_url = os.getenv('PICLOUD_SOCKET_URL')
        picloud_http_url = os.getenv('PICLOUD_HTTP_URL')
        picloud_api_key = os.getenv('PICLOUD_API_KEY')

        socket_client = SocketClient(
            url=picloud_socket_url,
            api_key=picloud_api_key,
            client_name='Test-Client')

        def on_event(data):
            self.assertEqual(data, 'test')

        socket_client.subscribe(event='whatever', callback=on_event)
        socket_client.publish(event='whatever', data='test')
        socket_client.process_subscriptions()

        http_client = HttpClient(
            url=picloud_http_url,
            api_key=picloud_api_key,
            client_name='Test-Client')

        http_client.publish(event='whatever', data='test')
        socket_client.process_subscriptions()
