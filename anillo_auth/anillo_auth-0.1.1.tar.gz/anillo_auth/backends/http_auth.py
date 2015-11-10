import re
import base64

from anillo.http.responses import Response


class HttpBasicAuthBackend:
    def __init__(self, auth_func):
        self.auth_regex = re.compile(r"^Basic: (.*)$")
        self.auth_func = auth_func

    def parse(self, request):
        authorization = request.headers.get("Authorization", None)
        if authorization is None:
            return None

        match = re.match(self.auth_regex, authorization)
        if match is None:
            return None

        try:
            auth_data = base64.b64decode(match.group(1).encode("utf-8")).decode()
            (username, password) = auth_data.split(":")
            return {"username": username, "password": password}
        except Exception:
            return None

    def authenticate(self, request, data):
        identity = self.auth_func(data["username"], data["password"])
        if isinstance(identity, Response):
            return identity

        request.identity = identity
        return request
