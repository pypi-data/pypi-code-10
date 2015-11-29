from collections import defaultdict
import requests
from picloud_client.connection import Connection


class PublishError(Exception):

    pass


class SubClient(object):

    def __init__(self, url, api_key, client_name):
        self.client_name = client_name
        self._connection = Connection(
            socket_url=url,
            api_key=api_key,
            client_name=self.client_name)
        self._subscriptions = defaultdict(list)

    def subscribe(self, event, callback):
        message = {
            'action': 'subscribe',
            'event': event
        }
        self._connection.send(message)
        self._subscriptions[event].append(callback)

    def process_subscriptions(self):
        message = self._connection.receive()
        for cb in self._subscriptions[message['event']]:
            cb(data=message['data'])


class PubClient(object):

    def __init__(self, url, api_key, client_name):
        self.client_name = client_name
        self._url = url
        self._api_key = api_key

    def publish(self, event, data):
        headers = {
            'X-API-Key': self._api_key,
            'X-API-Client-Name': self.client_name
        }
        body = {
            'event': event,
            'data': data
        }
        response = requests.post(self._url, json=body, headers=headers)
        if response.status_code != 201:
            raise PublishError
