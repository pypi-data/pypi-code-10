import os
import twitter
import curses

from polarbird.settings import settings
from polarbird.tokens import TOKENS_FILE, CONSUMER_KEY, CONSUMER_SECRET
from polarbird.tweets import TweetDatabase
from polarbird.windows import Screen
from polarbird.streams import UserStreamThread

class PolarBird(object):
    """
    Main class that everything starts. Creates OAuth instance for
    authentication to Twitter.
    """

    def __init__(self, screen):
        self.tweet_database = TweetDatabase()
        self.screen = Screen(screen, self)
        self._create_user_dir()
        self._auth = None
        self._stream_thread = UserStreamThread(self)

    def start_app(self):
        """
        Call for new stream thread for realtime tweets and start the app loop.
        """
        self._stream_thread.start()
        self._app_loop()

    @property
    def auth(self):
        """
        Read token file for tokens, if exists, or get new tokens from Twitter
        and return OAuth instance.
        """
        if not self._auth:
            if not os.path.exists(TOKENS_FILE):
                token, token_key = twitter.oauth_dance(
                    'PolarBird', CONSUMER_KEY,
                    CONSUMER_SECRET, TOKENS_FILE
                )
            else:
                token, token_key = twitter.read_token_file(TOKENS_FILE)
            self._auth = twitter.OAuth(
                token, token_key, CONSUMER_KEY, CONSUMER_SECRET
            )

        return self._auth

    def _create_user_dir(self):
        """
        Create user directory where settings and tokens are stored.
        """
        if not os.path.isdir(settings.USER_DIR):
            os.makedirs(settings.USER_DIR)

    def _app_loop(self):
        """
        Main app loop.
        """
        while True:
            self.screen.refresh_all_windows()
            character = self.screen.command_line_window.get_character()
            if character == curses.KEY_RESIZE:
                self.screen.handle_resize()
            else:
                self.screen.command_line_window.handle_input(character)
