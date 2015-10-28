import os
import pytest
from flask_bitjws import get_bitjws_header_payload
import bitjws
from example import server

wif = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"


def test_echo_details_request():
    privkey = bitjws.PrivateKey()
    echo_msg = 'hello'
    data = bitjws.sign_serialize(privkey, echo=echo_msg)
    app = server.app.test_client()
    echo = app.post('/echodetails', data=data, headers={'Content-Type': 'application/jose'})
    h, p = get_bitjws_header_payload(echo)
    assert 'alg' in h
    assert h['alg'] == 'CUSTOM-BITCOIN-SIGN'
    assert 'typ' in h
    assert 'kid' in h
    assert 'headers' in p['data']
    assert 'Content-Type' in p['data']['headers']
    assert p['data']['headers']['Content-Type'] == 'application/jose'
    assert 'jws' in p['data']
    rdata = p['data']['jws']
    assert 'payload' in rdata
    assert rdata['payload']['echo'] == echo_msg

