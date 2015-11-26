import json
from websocket import create_connection
from picloud_client.config import PICLOUD_API_KEY, PICLOUD_URL


class Connection(object):

    def __init__(self, client_name):
        url = '{0}?clientName={1}'.format(PICLOUD_URL, client_name)
        self._conn = create_connection(
            url=url,
            header=["X-API-Key: {0}".format(PICLOUD_API_KEY)])

    def send(self, message):
        self._conn.send(json.dumps(message))

    def receive(self):
        return json.loads(self._conn.recv())
