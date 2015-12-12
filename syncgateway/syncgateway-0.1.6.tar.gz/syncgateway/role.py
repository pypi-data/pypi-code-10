import json

from syncgateway import (errors, endpoint, urls)


class RoleEndpoint(endpoint.Endpoint):

    def get_list(self):
        query_url = urls.roles_url(self.database_url)
        response = self.session.get(query_url)

        if response.status_code == 200:
            return response.json()
        else:
            raise errors.UnexpectedResponseError(
                response.status_code,
                response.text
            )

    def get(self, role):
        query_url = urls.role_url(self.database_url, role)
        response = self.session.get(query_url)

        if response.status_code == 200:
            return response.json()
        else:
            raise errors.UnexpectedResponseError(
                response.status_code,
                response.text
            )

    def create(self, name, admin_channels=None):
        query_url = urls.roles_url(self.database_url)
        body = self._role_body(name, admin_channels)
        response = self.session.post(query_url, data=json.dumps(body))

        if response.status_code == 201:
            return True
        elif response.status_code == 409:
            return False
        else:
            raise errors.UnexpectedResponseError(
                response.status_code,
                response.text
            )

    def add_or_update(self, name, admin_channels=None):
        query_url = urls.role_url(self.database_url, name)
        body = self._role_body(name, admin_channels)
        response = self.session.put(query_url, data=json.dumps(body))

        if response.status_code >= 400:
            raise errors.ResponseError(
                "Error creating user",
                response.status_code,
                response.text
            )

    def delete(self, role):
        query_url = urls.role_url(self.database_url, role)
        response = self.session.delete(query_url)
        if response.status_code > 200:
            raise errors.UnexpectedResponseError(
                response.status_code,
                response.text
            )

    def _role_body(self, name, admin_channels):
        return {
            "name": name,
            "admin_cannels": admin_channels
        }
