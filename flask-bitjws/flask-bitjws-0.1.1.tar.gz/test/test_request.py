import os
import time
import json
import pytest
import bitjws
from example import server
from flask_bitjws import FlaskBitjws

wif = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"


def test_get_bitjws_header_payload():
    app = server.app.test_client()
    coins = app.get('/coin')
    h, p = bitjws.validate_deserialize(coins.get_data().decode('utf8'), requrl='/response')
    assert 'alg' in h
    assert h['alg'] == 'CUSTOM-BITCOIN-SIGN'
    assert 'typ' in h
    assert 'kid' in h
    assert 'data' in p
    assert isinstance(p['data'], list)
    assert 'metal' in p['data'][0] and 'mint' in p['data'][0]


def test_echo_request():
    privkey = bitjws.PrivateKey()
    pubkey = bitjws.pubkey_to_addr(privkey.pubkey.serialize())
    echo_msg = {'hello': 'server'}
    data = bitjws.sign_serialize(privkey, data=echo_msg, iat=time.time(), requrl="/echo")
    fbj = FlaskBitjws(server.app)
    app = server.app.test_client()
    udata = json.dumps({'username': pubkey[0:8], 'kid': pubkey})
    user = app.post('/user', data=udata)
    echo = app.post('/echo', data=data, headers={'Content-Type': 'application/jose'})
    h, p = bitjws.validate_deserialize(echo.get_data().decode('utf8'), requrl='/response')
    assert 'alg' in h
    assert h['alg'] == 'CUSTOM-BITCOIN-SIGN'
    assert 'typ' in h
    assert 'kid' in h
    assert 'data' in p
    assert p['data'] == echo_msg


def test_bad_nonce():
    app = server.app.test_client()
    privkey = bitjws.PrivateKey()
    echo_msg = {'hello': 'server'}
    data = bitjws.sign_serialize(privkey, echo=echo_msg, iat=time.time(), requrl="/echo")
    data2 = bitjws.sign_serialize(privkey, echo=echo_msg, iat=time.time()-2, requrl="/echo")
    echo = app.post('/echo', data=data, headers={'Content-Type': 'application/jose'})
    echo2 = app.post('/echo', data=data2, headers={'Content-Type': 'application/jose'})
    assert echo2.status_code == 401


def test_no_nonce():
    app = server.app.test_client()
    privkey = bitjws.PrivateKey()
    echo_msg = {'hello': 'server'}
    data = bitjws.sign_serialize(privkey, echo=echo_msg, requrl="/echo")
    echo = app.post('/echo', data=data, headers={'Content-Type': 'application/jose'})
    assert echo.status_code == 401


def test_bad_response():
    app = server.app.test_client()
    privkey = bitjws.PrivateKey()
    echo_msg = {'hello': 'server'}
    data = bitjws.sign_serialize(privkey, echo=echo_msg, iat=time.time(), requrl="/echo")
    data2 = bitjws.sign_serialize(privkey, echo='not%s' % echo_msg)
    da = data.split('.')
    da2 = data2.split('.')
    baddata = "%s.%s.%s" % (da[0], da2[1], da[2])
    echo = app.post('/echo', data=data, headers={'Content-Type': 'application/jose'})
    echo.data = baddata
    h, p = bitjws.validate_deserialize(echo.get_data().decode('utf8'), requrl='/response')
    assert h is None


def test_bad_request():
    app = server.app.test_client()
    privkey = bitjws.PrivateKey()
    echo_msg = {'hello': 'server'}
    data = bitjws.sign_serialize(privkey, echo=echo_msg, iat=time.time(), requrl="/echo")
    data2 = bitjws.sign_serialize(privkey, echo='not%s' % echo_msg)
    da = data.split('.')
    da2 = data2.split('.')
    baddata = "%s.%s.%s" % (da[0], da2[1], da[2])
    echo = app.post('/echo', data=baddata, headers={'Content-Type': 'application/jose'})
    assert echo.status_code == 401

