
import pytest
from beaker import crypto

import hashlib

def test_beaker_gen_keys():
    cleartext = u'user_foo\x00bogus_pwd'
    salt = u'x' * 32
    h = crypto.generateCryptoKeys(cleartext, salt, 10)

    cl2 = str(cleartext).encode('ascii', 'strict')
    print('ct %r' % cleartext)
    print('ct str %r' % str(cleartext))
    print('cl2 %r' % cl2)
    sa2 = str(salt).encode('ascii', 'strict')
    h2=hashlib.pbkdf2_hmac(hashlib.sha1().name, cl2, sa2, 10, None)
    print('hlib convert')
    print(h2)

    assert h == b'0F\x88S\x93\xa9\xf7\xb9f\xbf\x05\xf96\x95RL\x13\xfc\x8e\x0f\x0e\x96\xb3{sb\xbc+\xcbg6K'

def test_2():
    pass
