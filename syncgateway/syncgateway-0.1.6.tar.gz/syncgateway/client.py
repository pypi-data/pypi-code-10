import requests

from syncgateway import (session, user, role)


class Client(object):

    def __init__(self, admin_url=None, database=None, session=None):
        self._url = admin_url
        self._database = database
        self._session = session or requests.Session()
        self._session.headers.update(
            {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        self._configure_endpoints()
        super(Client, self).__init__()

    def _configure_endpoints(self):
        self.sessions = session.SessionEndpoint(
            self._url, self._database, self._session)
        self.users = user.UserEndpoint(
            self._url, self._database, self._session)
        self.roles = role.RoleEndpoint(
            self._url, self._database, self._session)

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value):
        self._database = value
        self._configure_endpoints()
