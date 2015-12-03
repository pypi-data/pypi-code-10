import hmac
import hashlib
from btcmagic import convert, ecdsa, hashes, ec

# Base58 header bytes
HD_HEADER_PRIVATE = b'\x04\x88\xAD\xE4'  # xprv
HD_HEADER_PUBLIC = b'\x04\x88\xB2\x1E'  # xpub

# Generate a random xpriv
def random_xpriv():
    priv = ecdsa.random_priv()
    chaincode = convert.random_bytes(32)
    return {
        'depth': 0,
        'fingerprint': b'\x00'*4,
        'i': 0,
        'chaincode': chaincode,
        'priv': priv
    }

# Get corresponding xpub from xpriv
def xpriv_to_xpub(k):
    return {
        'depth': k['depth'],
        'fingerprint': k['fingerprint'],
        'i': k['i'],
        'chaincode': k['chaincode'],
        'pub': ecdsa.priv_to_pub(k['priv'])
    }

def serialize_xpriv(k):
    b = b''
    b += HD_HEADER_PRIVATE
    b += convert.int_to_byte(k['depth'])
    b += k['fingerprint']
    b += convert.int_to_bytes(k['i'], 4)
    b += k['chaincode']
    b += b'\x00' + ecdsa.serialize_priv(k['priv'])
    return convert.bytes_to_b58check(b)

def deserialize_xpriv(data):
    dbin = convert.b58check_to_bytes(data)
    assert dbin[0:4] == HD_HEADER_PRIVATE

    return {
        'depth': dbin[4],
        'fingerprint': dbin[5:9],
        'i': convert.bytes_to_int(dbin[9:13]),
        'chaincode': dbin[13:45],
        'priv': ecdsa.deserialize_priv(dbin[46:78])
    }

def serialize_xpub(k):
    b = b''
    b += HD_HEADER_PUBLIC
    b += convert.int_to_byte(k['depth'])
    b += k['fingerprint']
    b += convert.int_to_bytes(k['i'], 4)
    b += k['chaincode']
    b += ecdsa.serialize_pub(k['pub'])
    return convert.bytes_to_b58check(b)

def deserialize_xpub(data):
    dbin = convert.b58check_to_bytes(data)
    assert dbin[0:4] == HD_HEADER_PUBLIC

    return {
        'depth': dbin[4],
        'fingerprint': dbin[5:9],
        'i': convert.bytes_to_int(dbin[9:13]),
        'chaincode': dbin[13:45],
        'pub': ecdsa.deserialize_pub(dbin[45:78])
    }

# Derivates child pub from parent pub
def derive_xpub(k, i):
    i = int(i)

    if i >= 2**31:
        raise Exception("Can't do private derivation on public key!")

    pub = k['pub']
    pub_ser = ecdsa.serialize_pub(pub)

    hmacdata = pub_ser + convert.int_to_bytes(i, 4)
    I = hmac.new(k['chaincode'], hmacdata, hashlib.sha512).digest()

    return {
        'depth': k['depth'] + 1,
        'fingerprint': hashes.hash160(pub_ser)[:4],
        'i': i,
        'chaincode': I[32:],
        'pub': ec.add(k['pub'], ecdsa.priv_to_pub(ecdsa.deserialize_priv(I[:32])))
    }

# Derivates child priv from parent priv
def derive_xpriv(k, i):
    i = int(i)

    pub = ecdsa.priv_to_pub(k['priv'])
    pub_ser = ecdsa.serialize_pub(pub)
    priv_ser = ecdsa.serialize_priv(k['priv'])

    if i >= 2**31:
        hmacdata = b'\x00' + priv_ser + convert.int_to_bytes(i, 4)
    else:
        hmacdata = pub_ser + convert.int_to_bytes(i, 4)

    I = hmac.new(k['chaincode'], hmacdata, hashlib.sha512).digest()

    return {
        'depth': k['depth'] + 1,
        'fingerprint': hashes.hash160(pub_ser)[:4],
        'i': i,
        'chaincode': I[32:],
        'priv': ec.add_scalar(k['priv'], ecdsa.deserialize_priv(I[:32]))
    }
