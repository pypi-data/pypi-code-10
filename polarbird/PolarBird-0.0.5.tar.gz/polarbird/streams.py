import threading
import twitter
import urllib

from polarbird.utils import show_notification

class StreamThread(threading.Thread):
    """
    Base class for Twitter streams for realtime tweets.
    """

    USER_DOMAIN = 'userstream.twitter.com'
    PUBLIC_DOMAIN = 'stream.twitter.com'

    def __init__(self, app):
        super(StreamThread, self).__init__()
        self.daemon = True
        self.reconnect = True
        self._app = app
        self._screen = self._app.screen

    def run(self):
        info_window = self._screen.get_window(self._screen.INFO_WINDOW)
        while self.reconnect:
            try:
                self._stream_loop()
            except twitter.TwitterHTTPError as e:
                info_window.add_message(
                    'Twitter error: {}'.format(str(e)), info_window.ERROR
                )
            except urllib.error.URLError as e:
                info_window.add_message(
                    'Url error: {}'.format(str(e)), info_window.ERROR
                )

    def _stream_loop(self):
        iterator = self._get_tweets_iterator()
        for tweet in iterator:
            if tweet.get('hangup'):
                info_window = self._screen.get_window(self._screen.INFO_WINDOW)
                info_window.add_message('Reconnecting to stream...')
                break
            elif tweet.get('text'):
                self._app.tweet_database.insert(tweet)
                show_notification(tweet)
                self._screen.get_window(self._screen.TWEET_WINDOW).refresh()

    def _get_domain(self):
        """
        Return domain to use with Stream API.
        """
        raise NotImplementedError

    def _get_tweets_iterator(self):
        """
        Return iterator for receiving new tweets.
        """
        raise NotImplementedError

    def _get_twitter_stream(self):
        """
        Returns TwitterStream instance.
        """
        stream = twitter.TwitterStream(
            auth=self._app.auth, domain=self._get_domain()
        )

        return stream

class UserStreamThread(StreamThread):

    def _get_domain(self):
        return UserStreamThread.USER_DOMAIN

    def _get_tweets_iterator(self):
        return self._get_twitter_stream().user()
