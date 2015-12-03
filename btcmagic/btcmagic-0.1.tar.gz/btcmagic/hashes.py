import hashlib

# Hashes
def ripemd160(s):
    assert isinstance(s, bytes)
    return hashlib.new('ripemd160', s).digest()

def sha256(s):
    assert isinstance(s, bytes)
    return hashlib.sha256(s).digest()

def hash256(s):
    return sha256(sha256(s))

def hash160(s):
    return ripemd160(sha256(s))
