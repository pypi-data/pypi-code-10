# -*- coding: utf-8 -*-

import unittest
from pykkelabels import *
#from pykkelabels import Pykkelabels
#from pykkelabels.exceptions import *

from decimal import *
import base64

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from os import path


def read_config():
    try:
        config = configparser.ConfigParser()
        if path.isfile('test/testsettings.ini'):
            config.read('test/testsettings.ini')
        elif path.isfile('testsettings.ini'):
            config.read('testsettings.ini')
        else:
            raise Exception('Missing testsettings.ini file')
        api_user = config.get('login', 'api_user')
        api_key = config.get('login', 'api_key')
        return api_user, api_key
    except:
        raise Exception('Unable to read the required settings from the ini file.')

class GoodInput(unittest.TestCase):

    def test_login(self):
        try:
            Pykkelabels(self.api_user, self.api_key)
        except urllib.error.HTTPError:
            self.fail('Did not log in properly')

    def test_balance(self):
        pl = Pykkelabels(self.api_user, self.api_key)
        self.assertEqual(Decimal(0.0), pl.balance())

    def test_getToken(self):
        pl = Pykkelabels(self.api_user, self.api_key)
        self.assertEqual(40, len(pl.getToken()))

    def test_pdkdroppoints(self):
        pl = Pykkelabels(self.api_user, self.api_key)
        exp_points = [{u'zipcode': u'2300', u'city': u'KØBENHAVN S', u'address': u'Brydes Allé 34', u'number': u'3830',
                       u'company_name': u'Pakkeboks 3830 Dagli Brugsen'},
                      {u'zipcode': u'2300', u'city': u'KØBENHAVN S', u'address': u'Englandsvej 28', u'number': u'626',
                       u'company_name': u'Pakkeboks 626 Kvickly'},
                      {u'zipcode': u'2300', u'city': u'KØBENHAVN S', u'address': u'Englandsvej 28', u'number': u'626',
                       u'company_name': u'Pakkeboks 626 Kvickly Handikapvenlig'}]
        points = pl.pdk_droppoints({'zipcode': '2300'})
        self.assertEqual(points, exp_points)

    def test_glsdroppoints(self):
        pl = Pykkelabels(self.api_user, self.api_key)
        exp_points = [{u'number': u'95913', u'city': u'København S', u'company_name': u'Dagli´Brugsen Brydes Allé',
                       u'address2': u'Pakkeshop: 95913', u'address': u'Brydes\xa0Allé 34', u'zipcode': u'2300'},
                      {u'number': u'95422', u'city': u'København S', u'company_name': u'PC Update',
                       u'address2': u'Pakkeshop: 95422', u'address': u'Amagerbrogade 109', u'zipcode': u'2300'},
                      {u'number': u'95423', u'city': u'København S', u'company_name': u'Centerkiosken',
                       u'address2': u'Pakkeshop: 95423', u'address': u'Reberbanegade 3', u'zipcode': u'2300'}]
        points = pl.gls_droppoints({'zipcode': '2300'})
        self.assertEqual(points, exp_points)

    def test_freight_rates(self):
        pl = Pykkelabels(self.api_user, self.api_key)
        rates = pl.freight_rates()

        # Test a couple of things, which should be in the returned dict
        self.assertIsInstance(rates, dict)
        self.assertIsInstance(rates['DK'], dict)
        self.assertIsInstance(rates['GB'], dict)
        self.assertIsInstance(rates['DE'], dict)
        self.assertIsInstance(rates['DK']['gls'], dict)
        self.assertIsInstance(rates['DK']['pdk'], dict)
        self.assertEqual(rates['DK']['pdk']['name'], 'Post Danmark')

    def test_payment_requests(self):
        pl = Pykkelabels(self.api_user, self.api_key)
        requests = pl.payment_requests()
        self.assertIsInstance(requests, list)
        self.assertEqual(0, len(requests))

    def test_create_shipment(self):
        params = {'shipping_agent': 'pdk',
                  'weight': '1000',
                  'receiver_name': 'John Doe',
                  'receiver_address1': 'Some Street 42',
                  'receiver_zipcode': '5230',
                  'receiver_city': 'Odense M',
                  'receiver_country': 'DK',
                  'receiver_email': 'test@test.dk',
                  'receiver_mobile': '12345678',
                  'sender_name': 'John Wayne',
                  'sender_address1': 'The Batcave 1',
                  'sender_zipcode': '5000',
                  'sender_city': 'Odense C',
                  'sender_country': 'DK',
                  'shipping_product_id': '51',
                  'services': '11,12',
                  'test': 'true'}

        pl = Pykkelabels(self.api_user, self.api_key)
        result = pl.create_shipment(params)
        self.assertEqual(result['pkg_no'], '00000000000000000000')
        self.assertEqual(result['order_id'], '0000')
        self.assertEqual(result['shipment_id'], '0000')

        # decode the data and cast it to bytearray to make it mutable
        pdf_payload = bytearray(base64.b64decode(result['base64']))
        pdf_payload[969:969+32] = b"00000000000000000000000000000000"  # blank out the date-stamp

        # get the reference label
        if path.isfile('reference_label.pdf'):
            ref_filename = 'reference_label.pdf'
        elif path.isfile(path.join('test', 'reference_label.pdf')):
            ref_filename = path.join('test', 'reference_label.pdf')
        else:
            raise Exception('Unable to locate the reference label file')

        with open(ref_filename, 'rb') as f:
            pdf_reference = f.read()

        self.assertEqual(pdf_payload, pdf_reference)

    def setUp(self):
        self.api_user, self.api_key = read_config()


class BadInput(unittest.TestCase):

    def test_login(self):
        self.assertRaises(PageError, Pykkelabels, 'Bad user', 'Bad key')

    def test_pdkdroppoints(self):
        pl = Pykkelabels(self.api_user, self.api_key)
        self.assertRaises(PageError, pl.pdk_droppoints, {'shouldbezipcode': '2300'})

    def test_glsdroppoints(self):
        pl = Pykkelabels(self.api_user, self.api_key)
        self.assertRaises(PageError, pl.gls_droppoints, {'shouldbezipcode': '2300'})

    def test_create_shipment(self):
        params = {'shipping_agent': 'pdk',
                  'weight': '1000',
                  'receiver_name': 'John Doe',
                  'receiver_address1': 'Some Street 42',
                  'receiver_zipcode': '5230',
                  'receiver_city': 'Odense M',
                  'receiver_country': 'DK',
                  'receiver_email': 'test@test.dk',
                  'receiver_mobile': '12345678',
                  'sender_name': 'John Wayne',
                  'sender_address1': 'The Batcave 1',
                  'sender_zipcode': '5000',
                  'sender_city': 'Odense C',
                  'sender_country': 'DK',
                  'shipping_product_id': '51',
                  'services': '11,123123',  # bad service number
                  'test': 'true'}

        pl = Pykkelabels(self.api_user, self.api_key)
        self.assertRaises(PageError, pl.create_shipment, params)

        params['services'] = '11,12'
        params['shipping_agent'] = 'BAD'
        self.assertRaises(PageError, pl.create_shipment, params)

    def test_bad_api_url(self):
        # Try with a bad domain name
        self.assertRaises(ConnError, Pykkelabels, self.api_user, self.api_key,
                          'https://app.pakkelabelsBADBAD.dk/api/public/v2')

        # Try with a bad url, but correct domain
        self.assertRaises(ConnError, Pykkelabels, self.api_user, self.api_key,
                          'https://app.pakkelabels.dk/api/public/v2BADBAD')

    def setUp(self):
        self.api_user, self.api_key = read_config()


if __name__ == '__main__':
    unittest.main()
