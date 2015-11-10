import re
from itsdangerous import JSONWebSignatureSerializer


class JWSBackend:
    def __init__(self, secret, token_name="Token"):
        self.token_regex = re.compile(r"^{}: (.*)$".format(token_name))
        self.serializer = JSONWebSignatureSerializer(secret)

    def parse(self, request):
        authorization = request.headers.get("Authorization", None)
        if authorization is None:
            return None

        match = re.match(self.token_regex, authorization)
        if match is None:
            return None

        sign = match.group(1)

        try:
            data = self.serializer.loads(sign)
            return data
        except Exception:
            return None

    def authenticate(self, request, data):
        request.identity = data
        return request
