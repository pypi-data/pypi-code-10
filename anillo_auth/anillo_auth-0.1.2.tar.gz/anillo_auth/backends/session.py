class SessionBackend:
    def parse(self, request):
        identity = request.get('session', {}).get('identity', None)
        if identity:
            return identity
        return None

    def authenticate(self, request, data):
        request.identity = data
        return request
