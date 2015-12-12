import json

from syncgateway import (errors, endpoint, urls)


class UserEndpoint(endpoint.Endpoint):

    def exists(self, username):
        query_url = urls.user_url(self.database_url, username)
        response = self.session.get(query_url)

        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            raise errors.UnexpectedResponseError(
                response.status_code,
                response.text
            )

    def get_list(self):
        query_url = urls.users_url(self.database_url)
        response = self.session.get(query_url)

        if response.status_code == 200:
            return response.json()
        else:
            raise errors.UnexpectedResponseError(
                response.status_code,
                response.text
            )

    def get(self, username):
        query_url = urls.user_url(self.database_url, username)
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

    def add_or_update(self,
                      username,
                      password=None,
                      name=None,
                      admin_channels=None,
                      admin_roles=None,
                      email=None,
                      disabled=None):
        query_url = urls.user_url(self.database_url, username)

        body = self._user_body(
            username,
            password,
            name,
            admin_channels,
            admin_roles,
            email,
            disabled
        )

        response = self.session.put(query_url, data=json.dumps(body))

        if response.status_code >= 400:
            raise errors.ResponseError(
                "Error creating user",
                response.status_code,
                response.text
            )

    def create(self,
               username,
               password=None,
               name=None,
               admin_channels=None,
               admin_roles=None,
               email=None,
               disabled=None):
        query_url = urls.users_url(self.database_url)

        body = self._user_body(
            username,
            password,
            name,
            admin_channels,
            admin_roles,
            email,
            disabled
        )

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

    def delete(self, username):
        query_url = urls.user_url(self.database_url, username)
        response = self.session.delete(query_url)
        if response.status_code > 200:
            raise errors.UnexpectedResponseError(
                response.status_code,
                response.text
            )

    def _user_body(self,
                   username,
                   password=None,
                   name=None,
                   admin_channels=None,
                   admin_roles=None,
                   email=None,
                   disabled=None):
        body = dict()
        if password:
            body["password"] = password
        if name:
            body["name"] = name
        if admin_channels:
            body["admin_channels"] = admin_channels
        if admin_roles:
            body["admin_roles"] = admin_roles
        if email:
            body["email"] = email
        if disabled:
            body["disabled"] = disabled

        return body
