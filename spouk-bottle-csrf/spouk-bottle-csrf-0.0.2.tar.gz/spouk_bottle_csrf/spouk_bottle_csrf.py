#!/usr/bin/env python
#coding: utf-8
__author__ = 'spouk'

from bottle import request
import random
import bs4
import functools
import hashlib
import uuid

class CSRF(object):
    name = "csrf"
    api = 2

    def __init__(self, parser='html.parser', csrf_salt=None):
        # type parser for parse html head for getting `META` csrf_token
        # see BS4 doc for descryption types available parsers
        self.parser = parser
        self.csrf_token = None
        self.csrf_token_last = None
        self.csrf_html = self._csrf_html
        self.app = None
        self.csrf_meta = None
        # some salt for strong hash :)
        self.csrf_salt = csrf_salt or random.gammavariate(10,200)

    def _csrf_html(self):
        """html widget for hidden csrf_token"""
        return "<input type='hidden' name='csrf_token' value='{}' >".format(self.csrf_token or request.environ('csrf_token', None))

    def setup(self, app):
        """setup plugin"""
        self.app = app
        self.app.csrf = self
        self.app.add_hook('before_request', self.generatetoken)

        # inject default keys
        request.environ['csrf_html'] = self.csrf_html
        request.environ['csrf_meta'] = self.csrf_meta
        request.environ['csrf_token'] = self.csrf_token
        request.environ['csrf_token_last'] = self.csrf_token_last

    def apply(self, callback, context):
        """apply plugin with current context application
        parse request body for get `META` csrf_token for AJAX requests for example..
        """
        def wrapper(*args, **kwargs):
            """wrapper for parse body request """

            # get `body` answer
            page = callback(*args, **kwargs)

            # parse `META` token
            pars_result = bs4.BeautifulSoup(page, self.parser).findAll('meta')
            found = filter(lambda x: x.get('name',None) and x.get('name') == 'csrf_token', pars_result)

            # update variable
            self.csrf_meta = found and found[0].get('content', None) or None
            request.environ['csrf_meta'] = self.csrf_meta

            return page
        return wrapper

    def generatetoken(self):
        """before request hook
            generate newtoken each request,
            if request `POST` save last token for compare `FORM`/`META` csrf_token
            SEND POST from user and origin true last csrf_token
            last token u can get `app.csrf.csrf_last_token` for compare
        """
        # if request method `POST` then save .last csrf_token for compare
        if request.method == "POST":
            self.csrf_token_last = self.csrf_token or None

        # make new csrf_token
        self.csrf_token= hashlib.md5(str(uuid.uuid4())+str(self.csrf_salt)).hexdigest()

        # update variables
        request.environ['csrf_token'] = self.csrf_token
        request.environ['csrf_html'] = self.csrf_html
