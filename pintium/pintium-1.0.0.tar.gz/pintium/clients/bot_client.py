from ..bot import Bot


class BotClient(object):
    """
    The BotClient is useful for obtaining most
    of the pin data, including the pin id. But,
    it is currently unable to obtain the create_at
    timestamp.  For that, just use the API client.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def search_for(self, *terms):
        bot = Bot().authenticate(self.username, self.password)
        bot.search_for(*terms)
        return bot
