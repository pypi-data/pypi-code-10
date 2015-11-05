# ======================= QuantGo Copyright Notice ============================
# Copyright 2013 QuantGo, LLC.  All rights reserved.
# Permission to use solely inside a QuantGo Virtual Quant Lab
# Written By: Nikolay
# Date: 12-12.2013
# ======================= QuantGo Copyright Notice ============================

# -*- coding: utf-8 -*-
"""Allows to calculate signature for request.
"""
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *
from future import standard_library
standard_library.install_aliases()
from builtins import object

import hashlib
import hmac
import base64

from urllib.parse import urlparse


class BaseSig(object):
    method = None

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def calculate(self):
        return NotImplementedError


class Sigv2(BaseSig):
    version = '2'
    method = 'hmacsha256'
    digestmod = hashlib.sha256

    def calculate(self, request_method, request_url):
        schema = urlparse(request_url)
        canonical = '\n'.join([request_method, schema.netloc,
                               schema.path or '/', schema.query])
        digest = hmac.new(self.secret_key.encode('utf-8'),
                          canonical.encode('utf-8'),
                          digestmod=self.digestmod).digest()
        signature = base64.b64encode(digest).decode()
        return signature
