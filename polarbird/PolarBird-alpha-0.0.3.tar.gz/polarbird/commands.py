class Command(object):
    """
    Base class for every command
    """

    NAME = None
    HELP_TEXT = None

    def __init__(self, app, info_window):
        if not self.NAME:
            raise ValueError(
                'NAME is not set for class {!r}'.format(self.__class__.__name__)
            )
        if not self.HELP_TEXT:
            raise ValueError(
                'HELP_TEXT is not set for class {!r}'.format(self.__class__.__name__)
            )
        self._app = app
        self._info_window = info_window

    def execute(self, t, args=None):
        raise NotImplementedError

class HomeCommand(Command):
    """
    Home command for home timeline view
    """

    NAME = 'home'
    HELP_TEXT = 'Shows home timeline for current logged user.'

    def execute(self, t, args=None):
        tweets = t.statuses.home_timeline()
        for tweet in reversed(tweets):
            self._app.tweet_database.insert(tweet)

class RetweetCommand(Command):
    """
    TODO: Fix retweet command.
    Command for retweeting based on Tweet index from TweetDatabase
    """

    NAME = 'rt'
    HELP_TEXT = 'Retweet a tweet.'

    def execute(self, t, args=None):
        if not args:
            pass
        else:
            self._retweet(t, args)

    def _retweet(self, t, args):
        try:
            tweet_id = self._app.tweet_database[args]['id']
            t.statuses.retweet(id=tweet_id, include_entities=False, trim_user=True)
        except KeyError:
            self._info_window.add_message(
                'Tweet id not found.', self._info_window.WARNING
            )

class WindowCommand(Command):
    """
    Command for window manipulation for example switching.
    """

    NAME = 'window'
    HELP_TEXT = 'Window manipulation.'

    def execute(self, t, args=None):
        if args == 'left':
            self._app.screen.switch_to_left_window()
        elif args == 'right':
            self._app.screen.switch_to_right_window()

        self._app.screen.refresh_current_window()
