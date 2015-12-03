from btcmagic import ec, convert
import hmac
import hashlib


# Key generation
def random_priv():
    return deserialize_priv(convert.random_bytes(32))

def priv_to_pub(priv):
    assert isinstance(priv, int)
    return ec.multiply(ec.G, priv)


def int_to_bytes_var_length(i):
    assert isinstance(i, int)
    return i.to_bytes((i.bit_length() // 8) + 1, byteorder='big')

# Encodings
def serialize_sig(sig):
    _, r, s = sig
    b1, b2 = int_to_bytes_var_length(r), int_to_bytes_var_length(s)
    left = b'\x02' + convert.int_to_byte(len(b1)) + b1
    right = b'\x02' + convert.int_to_byte(len(b2)) + b2
    return b'\x30' + convert.int_to_byte(len(left+right)) + left + right

def deserialize_sig(sig):
    leftlen = sig[3]
    left = sig[4:4+leftlen]
    rightlen = sig[5+leftlen]
    right = sig[6+leftlen:6+leftlen+rightlen]
    return (None, convert.bytes_to_int(left), convert.bytes_to_int(right))

def serialize_priv(priv):
    assert isinstance(priv, int)
    return convert.int_to_bytes(priv, 32)

def deserialize_priv(b):
    assert isinstance(b, bytes)
    return convert.bytes_to_int(b)

def serialize_pub(pub, compressed=True):
    if compressed:
        return convert.int_to_byte(2+(pub[1] % 2)) + convert.int_to_bytes(pub[0], 32)
    else:
        return b'\x04' + convert.int_to_bytes(pub[0], 32) + convert.int_to_bytes(pub[1], 32)


def deserialize_pub(b):
    x = convert.bytes_to_int(b[1:33])
    header = b[0]

    if header == 4:
        y = convert.bytes_to_int(b[33:65])
    else:
        beta = pow(int(x*x*x+ec.A*x+ec.B), int((ec.P+1)//4), int(ec.P))
        y = (ec.P-beta) if (beta + header) % 2 else beta

    return (x, y)



# ECDSA sign and verify

# https://tools.ietf.org/html/rfc6979#section-3.2
def deterministic_generate_k(msghash, priv):
    assert isinstance(msghash, bytes)
    assert len(msghash) == 32
    v = b'\x01' * 32
    k = b'\x00' * 32
    priv = serialize_priv(priv)
    k = hmac.new(k, v+b'\x00'+priv+msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v+b'\x01'+priv+msghash, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    v = hmac.new(k, v, hashlib.sha256).digest()
    return convert.bytes_to_int(v)

def sign(msghash, priv):
    assert isinstance(msghash, bytes)
    assert isinstance(priv, int)

    z = convert.bytes_to_int(msghash)
    k = deterministic_generate_k(msghash, priv)

    r, y = ec.multiply(ec.G, k)
    s = ec.inv(k, ec.N) * (z + r*priv) % ec.N

    # Ensure Low S constraint against tx malleability
    # https://github.com/bitcoin/bips/blob/master/bip-0062.mediawiki#Low_S_values_in_signatures
    if s > ec.N//2:
        s = ec.N - s
        y += 1   # Switch parity of y, otherwise recover breaks.

    return 27+(y % 2), r, s

def verify(msghash, sig, pub):
    assert isinstance(msghash, bytes)
    assert isinstance(sig, tuple)
    assert isinstance(pub, tuple)

    _, r, s = sig

    w = ec.inv(s, ec.N)
    z = convert.bytes_to_int(msghash)

    u1, u2 = z*w % ec.N, r*w % ec.N
    x, _ = ec.add(ec.multiply(ec.G, u1), ec.multiply(pub, u2))

    return r == x

# Recovers public key from signature and hash
def recover(msghash, sig):
    assert isinstance(msghash, bytes)
    assert isinstance(sig, tuple)
    v, r, s = sig
    x = r
    xcubedaxb = (x*x*x+ec.A*x+ec.B) % ec.P
    beta = pow(xcubedaxb, (ec.P+1)//4, ec.P)
    y = beta if v % 2 ^ beta % 2 else (ec.P - beta)
    # If xcubedaxb is not a quadratic residue, then r cannot be the x coord
    # for a point on the curve, and so the sig is invalid
    if (xcubedaxb - y*y) % ec.P != 0:
        return False
    z = convert.bytes_to_int(msghash)
    Gz = ec.jacobian_multiply((ec.Gx, ec.Gy, 1), (ec.N - z) % ec.N)
    XY = ec.jacobian_multiply((x, y, 1), s)
    Qr = ec.jacobian_add(Gz, XY)
    Q = ec.jacobian_multiply(Qr, ec.inv(r, ec.N))
    Q = ec.from_jacobian(Q)

    return Q
