from collections import defaultdict
from picloud_client.connection import Connection


class PiCloud(object):

    def __init__(self):
        self._connection = Connection()
        self._subscriptions = defaultdict(list)

    def publish(self, event, data):
        message = {
            'action': 'publish',
            'event': event,
            'data': data
        }
        self._connection.send(message)

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
