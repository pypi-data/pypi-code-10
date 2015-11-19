from contextlib import contextmanager
from selenium import webdriver

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

    def create_bot(self, session):
        return Bot(session).authenticate(self.username, self.password)

    @contextmanager
    def session(self):
        session = webdriver.Firefox()
        try:
            yield self.create_bot(session)
        finally:
            session.quit()

    def search_for(self, *terms):
        """
        WARNING: This method is deprecated.  Please use the
                 session() contextmanager instead.
        """
        bot = self.create_bot(webdriver.Firefox())
        bot.search_for(*terms)
        return bot
