import os
import pytest
import json
import time
import bitjws
from example import server
from flask_bitjws import FlaskBitjws

wif = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"


def test_echo_details_request():
    privkey = bitjws.PrivateKey()
    pubkey = bitjws.pubkey_to_addr(privkey.pubkey.serialize())
    echo_msg = {'hello': 'server'}
    data = bitjws.sign_serialize(privkey, data=echo_msg, iat=time.time(), requrl="/echodetails")
    fbj = FlaskBitjws(server.app)
    app = server.app.test_client()
    udata = json.dumps({'username': pubkey[0:8], 'kid': pubkey})
    user = app.post('/user', data=udata)
    echo = app.post('/echodetails', data=data, headers={'Content-Type': 'application/jose'})
    h, p = bitjws.validate_deserialize(echo.get_data().decode('utf8'), requrl='/response')
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
    assert rdata['payload']['data'] == echo_msg

