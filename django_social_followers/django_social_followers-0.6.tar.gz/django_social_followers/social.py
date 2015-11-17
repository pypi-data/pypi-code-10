import urllib
import urlparse
import subprocess

from django.conf import settings

import facebook
from instagram.client import InstagramAPI
import tweepy


class FacebookError(Exception):
    def __init__(self, message, errors):
        super(FacebookError, self).__init__(message)
        self.errors = 'Could not connect to Facebook'


class InstagramError(Exception):
    def __init__(self, message, errors):
        super(InstagramError, self).__init__(message)
        self.errors = 'Could not connect to Instagram'


class TwitterError(Exception):
    def __init__(self, message, errors):
        super(InstagramError, self).__init__(message)
        self.errors = 'Could not connect to Twitter'


class SocialFollowers():

    def __init__(self, **options):
        self.INSTAGRAM_SETTINGS = settings.INSTAGRAM_SETTINGS
        self.TWITTER_SETTINGS = settings.TWITTER_SETTINGS
        self.FACEBOOK_SETTINGS = settings.FACEBOOK_SETTINGS

    def get_facebook_followers(self, user):
        print 'get_facebook_followers', user
        oauth_args = {
            'client_id': self.FACEBOOK_SETTINGS['CLIENT_ID'],
            'client_secret': self.FACEBOOK_SETTINGS['CLIENT_SECRET'],
            'grant_type': self.FACEBOOK_SETTINGS['GRANT_TYPE']
        }
        oauth_curl_cmd = ['curl',
                          'https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(oauth_args)]
        oauth_response = subprocess.Popen(oauth_curl_cmd,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE).communicate()[0]

        try:
            oauth_access_token = urlparse.parse_qs(str(oauth_response))['access_token'][0]
        except KeyError:
            raise FacebookError
            exit()

        facebook_graph = facebook.GraphAPI(oauth_access_token)
        user = facebook_graph.get_object('/%s' % user)
        return user['likes']

    def get_twitter_followers(self, user):
        print 'get_twitter_followers', user
        try:
            auth = tweepy.OAuthHandler(self.TWITTER_SETTINGS['CONSUMER_KEY'], self.TWITTER_SETTINGS['CONSUMER_SECRET_KEY'])
            auth.set_access_token(self.TWITTER_SETTINGS['ACCESS_TOKEN_KEY'], self.TWITTER_SETTINGS['ACCESS_TOKEN_SECRET_KEY'])
            api = tweepy.API(auth)
            user = api.get_user(user)
            return user.followers_count
        except Exception as e:
            raise TwitterError

    def get_instagram_followers(self, user_id):
        print 'get_instagram_followers', user_id
        try:
            api = InstagramAPI(client_id=self.INSTAGRAM_SETTINGS['CLIENT_ID'], client_secret=self.INSTAGRAM_SETTINGS['CLIENT_SECRET'])
            user = api.user(user_id)
            return user.counts['followed_by']
        except Exception as e:
            raise InstagramError

