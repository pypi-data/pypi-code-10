from glob import glob
from os import path

try:
    from ._keccak import ffi
except ImportError:
    raise RuntimeError("Required CFFI extension not found. You need to install this package before use. See README.")


try:
    obj_name = glob(path.abspath(path.join(path.dirname(__file__), "sha3*")))[0]
except IndexError:
    raise RuntimeError("Required sha3 extension not found. You need to install this package before use. See README.")

lib = ffi.dlopen(obj_name)


class sha3_256(object):

    def __init__(self, seed=""):
        self.seed = seed

    def digest(self):
        return _sha3_256(self.seed)

    def hexdigest(self):
        return _sha3_256(self.seed).encode('hex')

    def update(self, string):
        self.seed = self.seed + string


class sha3_512(object):

    def __init__(self, seed=""):
        self.seed = seed

    def digest(self):
        return _sha3_512(self.seed)

    def hexdigest(self):
        return _sha3_512(self.seed).encode('hex')

    def update(self, string):
        self.seed = self.seed + string


# SHA3-256 hashing using the Keccak standard
def _sha3_256(seed):
    # Length of the output of sha256
    output_length = 32

    # ffi definition of the output uint array
    output = ffi.new("uint8_t[]", output_length)

    input_ = ffi.new("uint8_t[]", str(seed))

    lib.sha3_256(
        output,
        output_length,
        input_,
        len(seed)
    )

    buf = ffi.buffer(output, output_length)
    return buf[:]


# SHA3-512 hashing using the Keccak standard
def _sha3_512(seed):
    # Length of the output of sha512
    output_length = 64

    # ffi definition of the output uint array
    output = ffi.new("uint8_t[]", output_length)

    input_ = ffi.new("uint8_t[]", str(seed))

    lib.sha3_512(
        output,
        output_length,
        input_,
        len(seed)
    )

    buf = ffi.buffer(output, output_length)
    return buf[:]
