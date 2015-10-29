#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Cutting Edge QA

import json
import gspread
import re
import os
import robot
from robot.libraries.BuiltIn import BuiltIn
from oauth2client.client import SignedJwtAssertionCredentials


class CollectionsKeywordsExtension(object):
    def __init__(self):
        print "Start Collections"

    def create_dictionary_from_list(self, table):
        return dict((x, 0) for x in table)

    def create_dictionary_from_two_lists(self, keys, values):
        return dict(zip(keys, values))
