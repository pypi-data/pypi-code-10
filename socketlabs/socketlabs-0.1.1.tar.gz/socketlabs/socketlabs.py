import requests

from .constants import BASE_URL
from .exceptions import SocketLabsUnauthorized 

class SocketLabs():

    def __init__(self, username = None, password = None, serverid = None):

        self._username = username
        self._password = password
        self._serverid = serverid

    def failedMessages(self, **kwargs):

        url = BASE_URL + '/messagesFailed'

        headers = {'Accept': 'application/json'}
        params = {'serverId': self._serverid, 'type': 'json' }

        # Apply any custom parameters passed in
        for key, value in kwargs.items():
            params[key] = value

        r = requests.get(url, params = params, headers = headers, auth = (self._username, self._password))

        if r.status_code == 200:
            return r.json()
        else:
            raise SocketLabsUnauthorized(r)
