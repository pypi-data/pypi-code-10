import json
from websocket import create_connection


class Connection(object):

    def __init__(self, socket_url, api_key, client_name):
        url = '{0}?clientName={1}'.format(socket_url, client_name)
        self._conn = create_connection(
            url=url,
            header=["X-API-Key: {0}".format(api_key)])

    def send(self, message):
        self._conn.send(json.dumps(message))

    def receive(self):
        return json.loads(self._conn.recv())

    def close(self):
        self._conn.close()
