from collections import defaultdict
import requests
from picloud_client.connection import Connection


class PublishError(Exception):

    pass


class PiCloudClient(object):

    def __init__(self, url, api_key, client_name):
        self.url = url
        self.api_key = api_key
        self.client_name = client_name


class SocketClient(PiCloudClient):

    def __init__(self, url, api_key, client_name):
        super(SocketClient, self).__init__(
            url=url,
            api_key=api_key,
            client_name=client_name)
        self._sub_connection = Connection(
            socket_url='{0}/subscribe'.format(self.url),
            api_key=self.api_key,
            client_name=self.client_name)
        self._pub_connection = Connection(
            socket_url='{0}/publish'.format(self.url),
            api_key=self.api_key,
            client_name=self.client_name)
        self._subscriptions = defaultdict(list)

    def publish(self, event, data):
        message = {
            'event': event,
            'data': data
        }
        self._pub_connection.send(message)

    def subscribe(self, event, callback):
        message = {
            'action': 'subscribe',
            'event': event
        }
        self._sub_connection.send(message)
        self._subscriptions[event].append(callback)

    def process_subscriptions(self):
        message = self._sub_connection.receive()
        for cb in self._subscriptions[message['event']]:
            cb(data=message['data'])


class HttpClient(PiCloudClient):

    def __init__(self, url, api_key, client_name):
        super(HttpClient, self).__init__(
            url=url,
            api_key=api_key,
            client_name=client_name)

    def publish(self, event, data):
        headers = {
            'X-API-Key': self.api_key,
            'X-API-Client-Name': self.client_name
        }
        body = {
            'event': event,
            'data': data
        }
        response = requests.post(
            '{0}/publish'.format(self.url),
            json=body,
            headers=headers)
        if response.status_code != 201:
            raise PublishError
