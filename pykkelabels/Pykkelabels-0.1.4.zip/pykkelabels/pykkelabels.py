#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Python implementation of the Pakkelabels.dk php package for interacting with the Pakkelabels.dk web service.
For documentation on usage and the methods, see the documentation on https://www.pakkelabels.dk/integration/api/

Usage:
----------------
The first thing required is to login
label = new Pykkelabels('api_user', 'api_key')

This will login and fetch the required token.
The token is then automatically added to any subsequent calls.

To see the generated token you can use:
print(label.getToken())

Examples:
----------------
Get all Post Danmark labels shipped to Denmark:
labels = label.shipments({'shipping_agent': 'pdk', 'receiver_country': 'DK'})

Get the PDF for a specific label:
base64 = label.pdf(31629)
pdf = base64.decode('base64')
"""

import urllib.request
import urllib.error
import urllib.parse
import json
from decimal import *

from .exceptions import *


class Pykkelabels:
    API_ENDPOINT = 'https://app.pakkelabels.dk/api/public/v2'

    def __init__(self, api_user, api_key, api_endpoint=API_ENDPOINT):
        self._api_user = api_user
        self._api_key = api_key
        self._token = None
        self.api_endpoint = api_endpoint
        self.login()

    def login(self):
        result = self._make_api_call('users/login', True, {'api_user': self._api_user, 'api_key': self._api_key})
        self._token = result['token']

    def balance(self):
        result = self._make_api_call('users/balance')
        return Decimal(result['balance'])

    def pdf(self, idno):
        result = self._make_api_call('shipments/pdf', False, {'id': idno})
        return result['base64']

    def zpl(self, idno):
        result = self._make_api_call('shipments/zpl', False, {'id': idno})
        return result['base64']
    
    def shipments(self, params=None):
        result = self._make_api_call('shipments/shipments', False, params)
        return result
    
    def imported_shipments(self, params=None):
        result = self._make_api_call('shipments/imported_shipments', False, params)
        return result

    def create_imported_shipment(self, params):
        result = self._make_api_call('shipments/imported_shipment', True, params)
        return result
    
    def create_shipment(self, params):
        result = self._make_api_call('shipments/shipment', True, params)
        return result

    def create_shipment_own_customer_number(self, params):
        result = self._make_api_call('shipments/shipment_own_customer_number', True, params)
        return result

    def freight_rates(self):
        result = self._make_api_call('shipments/freight_rates')
        return result

    def payment_requests(self):
        result = self._make_api_call('users/payment_requests')
        return result

    def gls_droppoints(self, params):
        result = self._make_api_call('shipments/gls_droppoints', False, params)
        return result

    def pdk_droppoints(self, params):
        result = self._make_api_call('shipments/pdk_droppoints', False, params)
        return result

    def getToken(self):
        return self._token

    def _make_api_call(self, method, doPost=False, params=None):
        if params is None:
            params = dict()
        elif not isinstance(params, dict):
            raise TypeError('params should be of type dict or None, got type: {}'.format(type(params).__name__))

        params['token'] = self._token
        params = urllib.parse.urlencode(params)

        try:
            if doPost:
                url = self.api_endpoint + '/' + method
                f = urllib.request.urlopen(url, params.encode('utf-8'))
            else:
                url = self.api_endpoint + '/' + method + '?' + params
                f = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            error_message = e.read().decode('utf-8')
            try:
                error_parsed = json.loads(error_message)
            except:
                raise URLError('Parsed error message is not parsable, possible bad url')
            if isinstance(error_parsed['message'], dict):
                error_message = error_parsed['message']['base'][0]
            else:
                error_message = error_parsed['message']
            message = str(e) + '; ' + error_message
            raise HTTPError(message) from None
            return None
        except urllib.error.URLError as e:
            raise URLError('URL error: {}'.format(e.reason)) from None
            return None

        output = f.read().decode('utf-8')
        outputparsed = json.loads(output)
        
        return outputparsed
