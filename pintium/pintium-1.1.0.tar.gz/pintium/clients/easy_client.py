from .bot_client import BotClient
from .api_client import APIClient


class EasyClient(object):
    def __init__(self, username, password, token):
        self.bot_client = BotClient(username, password)
        self.api_client = APIClient(token)

    def search_for(self, *terms):
        pins = self.bot_client.search_for(*terms)

        def full_details():
            for p in pins:
                pin_id = p.pin_id
                if pin_id:
                    yield self.api_client.get_pin(pin_id)["data"]

        return full_details()
