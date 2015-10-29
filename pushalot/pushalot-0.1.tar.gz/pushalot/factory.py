from pushalot.apis import (
    BaseAPI,
    APILatest,
)
from pushalot.transport import (
    PushalotTransportInterface,
    HTTPTransport,
)

class PushalotFactory(object):

    @classmethod
    def create(cls, token, api=None, transport=None):
        if transport is not None:
            if not issubclass(transport, PushalotTransportInterface):
                raise RuntimeError(
                    "Transport should be subclass of PushalotTransportInterface"
                )
        else:
            transport = HTTPTransport()

        if api is not None:
            if not issubclass(api, BaseAPI):
                raise RuntimeError(
                    'API class should be subclass of BaseAPI'
                )
        else:
            api = APILatest(transport=transport, token=token)

        return api
