# -*- coding: utf-8 -*-
# Copyright © 2015 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/

# Main class
'''Main class'''

import configparser
import os.path
import sys
import tweepy

from retweet.cliparse import CliParse
from retweet.confparse import ConfParse
from retweet.tweetwasposted import TweetWasPosted
from retweet.waitamoment import WaitAMoment


class Main(object):
    '''Main class'''
    def __init__(self):
        '''Constructor of the Main class'''
        # parse the command line
        rtargs = CliParse()
        pathtoconf = rtargs.configfile
        # read the configuration file
        cfgparse = ConfParse(pathtoconf)
        self.cfgvalues = cfgparse.confvalues

        # activate the twitter api
        self.auth = tweepy.OAuthHandler(self.cfgvalues['consumer_key'],
                                        self.cfgvalues['consumer_secret'])
        self.auth.secure = True
        self.auth.set_access_token(self.cfgvalues['access_token'],
                                    self.cfgvalues['access_token_secret'])
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.main()

    def main(self):
        '''Main of the Main class'''
        # get the 20 last tweets
        lasttweets = self.api.user_timeline(self.cfgvalues['user_to_retweet'])
        # see if the last tweet of twitter api was sent already
        lasttweetid = lasttweets[-1].id
        self.twp = TweetWasPosted(self.cfgvalues)
        # extract the last 20 tweet ids
        lasttweetids = [tweet.id for tweet in lasttweets]
        lasttweetids.reverse()
        tweetstosend = []
        # test if the last 20 tweets were posted
        for lasttweet in lasttweetids:
            if not self.twp.wasposted(lasttweet):
                self.sendthetweet(lasttweet)
        sys.exit(0)

    def sendthetweet(self, tweet):
        '''send the tweet'''
        try:
            # test if it was retweeted enough to be retweeted by me
            if len(self.api.retweets(tweet)) >= self.cfgvalues['retweets']:
                # test if the tweet has a hashtag for not retweeting it
                if not self.notretweethashes(tweet):
                    self.api.retweet(tweet)
                    #print("tweet {} sent!".format(tweet))
        except (tweepy.error.TweepError) as err:
            print("{}".format(err))
            print("the tweet is probably retweeted already. Twitter does not allow to retweet 2 times")
        finally:
            # now store the tweet
            if not self.twp.wasposted(tweet):
                self.twp.storetweet(tweet)
                WaitAMoment(self.cfgvalues['waitminsecs'], self.cfgvalues['waitmaxsecs'])

    def notretweethashes(self, tweet):
        '''check if the tweet has a hash for not retweeting'''
        found = False
        # check if the current tweet contains a do-not-retweet hash
        for i in self.cfgvalues['dontretweethashes']:
            if '#{}'.format(i) in self.api.get_status(tweet).text:
                found = True
        return found
