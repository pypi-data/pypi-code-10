import os
import pytest
from flask_bitjws import Application
import bitjws
from example import server

wif = "KweY4PozGhtkGPMvvD7vk7nLiN6211XZ2QGxLBMginAQW7MBbgp8"


def test_init_WIF():
    app = Application(__name__, privkey=wif)
    assert wif == bitjws.privkey_to_wif(app._privkey.private_key)


def test_init_PrivateKey():
    privkey = bitjws.PrivateKey(bitjws.wif_to_privkey(wif))
    app = Application(__name__, privkey=privkey)
    assert wif == bitjws.privkey_to_wif(app._privkey.private_key)

