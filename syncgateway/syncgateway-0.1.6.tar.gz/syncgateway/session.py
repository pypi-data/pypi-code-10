import json

from syncgateway import (errors, endpoint, urls)


class SessionEndpoint(endpoint.Endpoint):

    def get(self, session_id):
        query_url = urls.session_url(self.database_url, session_id)
        response = self.session.get(query_url)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return None
        else:
            raise errors.UnexpectedResponseError(
                response.status_code,
                response.text
            )

    def create(self, username, ttl=None):
        query_url = urls.sessions_url(self.database_url)

        SECONDS_IN_DAY = 86400
        body = {
            "name": username,
            "ttl": ttl or SECONDS_IN_DAY
        }
        response = self.session.post(query_url, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            raise errors.UnexpectedResponseError(
                response.status_code,
                response.text
            )

    def delete(self, session_id=None, username=None):
        query_url = urls.session_delete_url(
            self.database_url, session_id, username
        )
        response = self.session.delete(query_url)
        if response.status_code > 200:
            raise errors.UnexpectedResponseError(
                response.status_code,
                response.text
            )
