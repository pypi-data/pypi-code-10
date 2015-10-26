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

from db2twitter.cliparse import CliParse
from db2twitter.confparse import ConfParse
from db2twitter.dbparse import DbParse
from db2twitter.twbuild import TwBuild
from db2twitter.twsend import TwSend

class Main(object):
    '''Main class'''
    def __init__(self):
        '''Constructor of the Main class'''
        self.main()

    def main(self):
        '''Main of the Main class'''
        # parse the command line
        rtargs = CliParse()
        pathtoconf = rtargs.configfile
        # read the configuration file
        cfgparse = ConfParse(pathtoconf)
        cfgvalues = cfgparse.confvalues
        # parse the database
        dbparse = DbParse(cfgvalues)
        dbvalues = dbparse.dbvalues
        # prepare the tweet
        twbuild = TwBuild(cfgvalues, dbvalues)
        tweet = twbuild.readytotweet
        # send the tweet
        twsend = TwSend(cfgvalues, tweet)
