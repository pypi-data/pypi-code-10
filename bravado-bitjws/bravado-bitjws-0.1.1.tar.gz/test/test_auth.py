import bitjws
import json
import os
import pytest
import requests
import time
from bravado.swagger_model import load_file
from bravado_bitjws.client import BitJWSSwaggerClient
from bravado_bitjws.requests_client import *

specurl = "%s/example/swagger.json" % os.path.realpath(os.path.dirname(__file__))
wif = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"


def test_apply_auth():
    url = 'http://0.0.0.0:8002/path/to/api'
    bjauth = BitJWSAuthenticator('0.0.0.0', privkey=wif)
    data = ""
    headers = {}
    params = {'message': 'goes here for sure'}
    request = requests.Request(method='GET', url=url, headers=headers,
                               data=data, params=params)
    req = bjauth.apply(request)
    assert len(req.params) == 0
    assert req.headers['content-type'] == 'application/jose'

    h, p = bitjws.validate_deserialize(req.data, requrl=url)
    assert 'message' in p['data']
    assert p['data']['message'] == params['message']
    assert 'aud' in p
    assert p['aud'] == url


def test_apply_auth_json():
    url = 'http://0.0.0.0:8002/path/to/api'
    bjauth = BitJWSAuthenticator('0.0.0.0', privkey=wif)
    rawdata = {'message': 'goes here for sure'}
    data = json.dumps(rawdata)
    headers = {'content-type': 'application/json'}
    params = {'mess': 'couldgohere'}
    request = requests.Request(method='GET', url=url, headers=headers,
                               data=data, params=params)
    req = bjauth.apply(request)
    assert len(req.params) == 0
    assert req.headers['content-type'] == 'application/jose'

    h, p = bitjws.validate_deserialize(req.data, requrl=url)
    assert 'message' in p['data']
    assert p['data']['message'] == rawdata['message']


def test_response_good():
    bjauth = BitJWSAuthenticator('0.0.0.0', privkey=wif)

    headers = {'content-type': 'application/jose'}
    params = {'mess': 'goeshere'}

    data = bitjws.sign_serialize(bjauth.privkey, requrl="/response",
                                 iat=time.time(),
                                 data=params)

    resp = requests.models.Response()
    resp.status_code = 200
    resp._content = b'%s' % data
    resp.headers = headers

    response = BitJWSRequestsResponseAdapter(resp)
    assert response.json() == params


def test_response_json():
    bjauth = BitJWSAuthenticator('0.0.0.0', privkey=wif)

    headers = {'content-type': 'application/json'}
    params = {'mess': 'goeshere'}

    data = json.dumps(params)

    resp = requests.models.Response()
    resp.status_code = 200
    resp._content = b'%s' % data
    resp.headers = headers

    response = BitJWSRequestsResponseAdapter(resp)
    assert response.json() == params


def test_response_bad_requrl():
    bjauth = BitJWSAuthenticator('0.0.0.0', privkey=wif)

    headers = {'content-type': 'application/jose'}
    params = {'mess': 'couldgohere'}

    data = bitjws.sign_serialize(bjauth.privkey, requrl="/request/not/response",
                                 iat=time.time(),
                                 data=params)

    resp = requests.models.Response()
    resp.status_code = 200
    resp._content = b'%s' % data
    resp.headers = headers

    response = BitJWSRequestsResponseAdapter(resp)
    pytest.raises(bitjws.jws.InvalidPayload, response.json)

