
import hashlib
import binascii
import json
from cork import Cork
import base64
from base64 import b64encode

import pytest
from beaker import crypto


def test_hash_basic_sha1():
    dk = hashlib.pbkdf2_hmac('sha1', b'password', b'salt', 100000)
    assert binascii.hexlify(dk) == b'f5496bb1328184f5228eff393ab4be9ae8fe69e7'

def test_hash_basic_sha1_b():
    dk = hashlib.pbkdf2_hmac('sha1', b'password', b'salt', 10)
    assert binascii.hexlify(dk) == b'ae3fe5f5707e07f3e7c117fb885cd052a6fcd77a'

def test_hash_basic_sha1_c():
    cleartext = b'x' * 32
    salt = b'y' * 32
    dk = hashlib.pbkdf2_hmac('sha1', b'password', salt, 10)
    h_old = crypto.generateCryptoKeys(cleartext, salt, 10)
    assert binascii.hexlify(dk) == b'b10d37a81afb93afa5db8b522dc5cf8d8164f469'
    assert binascii.hexlify(h_old) == b'b10d37a81afb93afa5db8b522dc5cf8d8164f469'


def test_hash():
    cleartext = b'x' * 32
    salt = b'y' * 32
    print(repr(cleartext))
    h = hashlib.pbkdf2_hmac('sha1', cleartext, salt, 10)
    h = binascii.hexlify(h)
    assert h == b'916c7f92b887a3eace655172bc3ed21fcecd82ef'

def test_hash_32():
    cleartext = b'x' * 32
    salt = b'y' * 32
    h = hashlib.pbkdf2_hmac('sha1', cleartext, salt, 10, dklen=32)
    h = binascii.hexlify(h)
    assert h == b'916c7f92b887a3eace655172bc3ed21fcecd82ef4b28c12826cd5cada361013f'


def test_compare_pbkdf2():
    cleartext = b'x' * 32
    salt = b'y' * 32
    old_h = crypto.generateCryptoKeys(cleartext, salt, 10)
    h = hashlib.pbkdf2_hmac('sha1', cleartext, salt, 10, dklen=32)
    assert len(h) == len(old_h)
    assert h == old_h



# Test PBKDF2-based password hashing

_hash = Cork._hash_pbkdf2

def _oldhash(username, pwd, salt=None):
    username = username.encode('utf-8')
    pwd = pwd.encode('utf-8')
    cleartext = username + b'\0' + pwd
    h = crypto.generateCryptoKeys(cleartext, salt, 10)
    hashed = b'p' + salt + h
    return b64encode(hashed)

def test_password_hashing_PBKDF2():
    shash = _hash(u'user_foo', u'bogus_pwd')
    shash_old = _oldhash(u'user_foo', u'bogus_pwd')
    assert isinstance(shash, bytes)
    assert len(shash) == 88, "hash length should be 88 and is %d" % len(shash)
    assert shash.endswith(b'='), "hash should end with '='"
    assert shash == shash_old


def test_password_hashing_PBKDF2_known_hash():
    salt = b's' * 32
    shash = _hash(u'user_foo', u'bogus_pwd', salt=salt)
    shash_old = _oldhash(u'user_foo', u'bogus_pwd', salt=salt)
    assert shash == 'cHNzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzax44AxQgK6uD9q1YWxLos1ispCe1Z7T7pOFK1PwdWEs='
    assert shash == shash_old


def test_password_hashing_PBKDF2_known_hash_2():
    salt = b'\0' * 32
    shash = _hash(u'user_foo', u'bogus_pwd', salt=salt)
    shash_old = _oldhash(u'user_foo', u'bogus_pwd', salt=salt)
    assert shash == 'cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/8Uh4pyEOHoRz4j0lDzAmqb7Dvmo8GpeXwiKTDsuYFw='
    assert shash == shash_old


def test_password_hashing_PBKDF2_known_hash_3():
    salt = b'x' * 32
    shash = _hash(u'user_foo', u'bogus_pwd', salt=salt)
    shash_old = _oldhash(u'user_foo', u'bogus_pwd', salt=salt)
    assert shash == b'cHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4MEaIU5Op97lmvwX5NpVSTBP8jg8OlrN7c2K8K8tnNks='
    assert shash == shash_old


def test_password_hashing_PBKDF2_incorrect_hash_len():
    salt = b'x' * 31 # Incorrect length
    with pytest.raises(AssertionError):
        shash = _hash(u'user_foo', u'bogus_pwd', salt=salt)


def test_password_hashing_PBKDF2_incorrect_hash_value():
    shash = _hash(u'user_foo', u'bogus_pwd')
    assert len(shash) == 88, "hash length should be 88 and is %d" % len(shash)
    assert shash.endswith(b'='), "hash should end with '='"


def test_password_hashing_PBKDF2_collision():
    salt = b'S' * 32
    hash1 = _hash(u'user_foo', u'bogus_pwd', salt=salt)
    hash2 = _hash(u'user_foobogus', u'_pwd', salt=salt)
    assert hash1 != hash2, "Hash collision"


