import os
import pytest
from flask_bitjws import get_bitjws_header_payload
import bitjws
from example import server

wif = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"


def test_get_bitjws_header_payload():
    app = server.app.test_client()
    coins = app.get('/coin')
    h, p = get_bitjws_header_payload(coins)
    assert 'alg' in h
    assert h['alg'] == 'CUSTOM-BITCOIN-SIGN'
    assert 'typ' in h
    assert 'kid' in h
    assert 'data' in p
    assert isinstance(p['data'], list)
    assert 'metal' in p['data'][0] and 'mint' in p['data'][0]


def test_echo_request():
    privkey = bitjws.PrivateKey()
    echo_msg = 'hello'
    data = bitjws.sign_serialize(privkey, echo=echo_msg)
    app = server.app.test_client()
    echo = app.post('/echo', data=data)
    h, p = get_bitjws_header_payload(echo)
    assert 'alg' in h
    assert h['alg'] == 'CUSTOM-BITCOIN-SIGN'
    assert 'typ' in h
    assert 'kid' in h
    assert 'data' in p
    assert isinstance(p['data'], unicode)
    assert p['data'] == echo_msg


def test_bad_request():
    app = server.app.test_client()
    privkey = bitjws.PrivateKey()
    echo_msg = 'hello'
    data = bitjws.sign_serialize(privkey, echo=echo_msg)
    data2 = bitjws.sign_serialize(privkey, echo='not%s' % echo_msg)
    da = data.split('.')
    da2 = data2.split('.')
    baddata = "%s.%s.%s" % (da[0], da2[1], da[2])
    echo = app.post('/echo', data=data)  # how else to create a response?
    echo.data = baddata
    h, p = get_bitjws_header_payload(echo)
    assert h is None

