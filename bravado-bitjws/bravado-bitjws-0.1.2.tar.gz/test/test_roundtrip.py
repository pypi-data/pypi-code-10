import bitjws
import httpretty
import json
import os
import pytest
import time
from bravado.swagger_model import load_file
from bravado_bitjws.client import BitJWSSwaggerClient
from bravado_bitjws.requests_client import BitJWSAuthenticator

specurl = "%s/example/swagger.json" % os.path.realpath(os.path.dirname(__file__))
wif = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"

def test_good_call():
    url = 'http://0.0.0.0:8002/coin'
    bjauth = BitJWSAuthenticator('0.0.0.0', privkey=wif)
    client = BitJWSSwaggerClient.from_spec(load_file(specurl),
                                           origin_url=url, privkey=wif)
    coin = [{'metal':'m', 'mint':'n'}]

    data = bitjws.sign_serialize(bjauth.privkey, requrl="/response",
                                 iat=time.time(),
                                 data=coin)

    httpretty.enable()
    httpretty.register_uri(httpretty.GET, url,
                           body=data, content_type = 'application/jose')

    resp = client.coin.findCoin().result()
    assert resp[0].metal == coin[0]['metal']
    assert resp[0].mint == coin[0]['mint']

    httpretty.disable()
    httpretty.reset()

