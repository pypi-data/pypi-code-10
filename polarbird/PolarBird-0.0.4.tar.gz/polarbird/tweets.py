from collections import OrderedDict
from itertools import cycle

ALPHABET = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
)
NUMBERS = list(range(0, 10))

def generate_tweet_keys():
    for character in ALPHABET:
        for number in NUMBERS:
            yield '{}{}'.format(character, number)

class TweetDatabase(object):
    """
    Dictionary like object for temporary storing tweets with
    a-z0-9 indexing
    """

    TWEET_KEYS = cycle(generate_tweet_keys())

    def __init__(self):
        self._tweets = OrderedDict()

    def insert(self, tweet):
        """
        Add tweet to database. If tweet already exist in database,
        put it to end.
        """
        key = next(self.TWEET_KEYS)
        if (key in self._tweets):
            del self._tweets[key]

        self._tweets[key] = tweet

        return key

    def keys(self):
        """
        Returns all keys from tweet dictionary.
        """
        keys = self._tweets.keys()
        return list(keys)

    def __getitem__(self, key):
        return self._tweets[key]

    def __len__(self):
        return len(self._tweets)

    def __repr__(self):
        return str(self._tweets)

    def __setitem__(self, key, tweet):
        raise NotImplementedError
