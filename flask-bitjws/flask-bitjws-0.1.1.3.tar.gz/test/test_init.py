import os
import pytest
from flask import Flask
from flask_bitjws import FlaskBitjws
import bitjws
from example import server

wif = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"


def test_init_WIF():
    app = Flask(__name__)
    fbj = FlaskBitjws(app, privkey=wif)
    assert wif == bitjws.privkey_to_wif(app.bitjws._privkey.private_key)


def test_init_PrivateKey():
    privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(wif))
    app = Flask(__name__)
    fbj = FlaskBitjws(app, privkey=privkey)
    assert wif == bitjws.privkey_to_wif(app.bitjws._privkey.private_key)

