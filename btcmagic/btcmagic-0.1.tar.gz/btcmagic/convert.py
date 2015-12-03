import os
import binascii
from btcmagic import hashes

# Conversions
def hex_to_bytes(s):
    assert isinstance(s, str)
    return bytes.fromhex(s)

def bytes_to_hex(a):
    assert isinstance(a, bytes)
    return str(binascii.hexlify(a), 'utf-8')

def string_to_bytes(a):
    assert isinstance(a, str)
    return bytes(a, 'utf-8')

def bytes_to_string(a):
    assert isinstance(a, bytes)
    return a.decode("utf-8")

# Convert big integers to/from their big endian bytes representation.
def int_to_bytes(i, l):
    assert isinstance(i, int)
    return i.to_bytes(l, byteorder='big')

def bytes_to_int(b):
    assert isinstance(b, bytes)
    return int.from_bytes(b, byteorder='big')

def int_to_bytes_le(i, l):
    assert isinstance(i, int)
    return i.to_bytes(l, byteorder='little')

def bytes_to_int_le(b):
    assert isinstance(b, bytes)
    return int.from_bytes(b, byteorder='little')

# Convert single-byte integer to/from a 1-byte bytes object
def int_to_byte(i):
    assert isinstance(i, int)
    return bytes([i])

def byte_to_int(b):
    assert isinstance(b, bytes)
    assert len(b) == 1
    return b[0]


# Random
def random_bytes(l):
    return os.urandom(l)

B58_CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
B58_CHARS_REV = {c:i for i,c in enumerate(B58_CHARS)}

# Base58 encodings
def bytes_to_b58(b):
    assert isinstance(b, bytes)

    leadingzbytes = 0
    for x in b:
        if x != 0:
            break
        leadingzbytes += 1

    n = bytes_to_int(b)
    r = []
    while n > 0:
        r.append(B58_CHARS[n % 58])
        n //= 58

    return '1' * leadingzbytes + ''.join(r[::-1])

def b58_to_bytes(b):
    leadingzbytes = 0
    for x in b:
        if x != '1':
            break
        leadingzbytes += 1

    n = 0
    for c in b:
        n *= 58
        n += B58_CHARS_REV[c]

    data = n.to_bytes((n.bit_length()+7)// 8, byteorder='big')
    return b'\x00' * leadingzbytes + data

def bytes_to_b58check(b):
    assert isinstance(b, bytes)
    b += hashes.hash256(b)[:4]
    return bytes_to_b58(b)

def b58check_to_bytes(b):
    data = b58_to_bytes(b)
    assert hashes.hash256(data[:-4])[:4] == data[-4:]
    return data[:-4]

def pub_to_addr(pub):
    assert isinstance(pub, bytes)
    return hash_to_addr(hashes.hash160(pub))

def hash_to_addr(h):
    assert isinstance(h, bytes)
    assert len(h) == 20
    return bytes_to_b58check(b'\x00'+h)

def addr_to_hash(addr):
    assert isinstance(addr, str)
    b = b58check_to_bytes(addr)
    assert len(b) == 21
    assert b[0] == 0
    return b[1:]
