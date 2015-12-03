from btcmagic import ecdsa, convert, script, hashes
import copy
from enum import Enum

# Deserializes a transaction from its bytes representation
def deserialize(tx):
    assert isinstance(tx, bytes)
    # http://stackoverflow.com/questions/4851463/python-closure-write-to-variable-in-parent-scope
    # Python's scoping rules are demented, requiring me to make pos an object
    # so that it is call-by-reference
    pos = [0]

    def read_as_int(bytez):
        pos[0] += bytez
        return convert.bytes_to_int_le(tx[pos[0]-bytez:pos[0]])

    def read_var_int():
        pos[0] += 1

        val = tx[pos[0]-1]
        if val < 253:
            return val
        return read_as_int(pow(2, val - 252))

    def read_bytes(bytez):
        pos[0] += bytez
        return tx[pos[0]-bytez:pos[0]]

    def read_var_string():
        size = read_var_int()
        return read_bytes(size)

    obj = {"ins": [], "outs": []}
    obj["version"] = read_as_int(4)
    ins = read_var_int()
    for _ in range(ins):
        obj["ins"].append({
            "outpoint": {
                "hash": read_bytes(32)[::-1],
                "index": read_as_int(4)
            },
            "script": read_var_string(),
            "sequence": read_as_int(4)
        })
    outs = read_var_int()
    for _ in range(outs):
        obj["outs"].append({
            "value": read_as_int(8),
            "script": read_var_string()
        })
    obj["locktime"] = read_as_int(4)
    return obj

def encode_var_int(x):
    x = int(x)
    if x < 253: return convert.int_to_byte(x)
    elif x < 65536: return convert.int_to_byte(253) + convert.int_to_bytes_le(x, 2)
    elif x < 4294967296: return convert.int_to_byte(254) + convert.int_to_bytes_le(x, 4)
    else: return convert.int_to_byte(255) + convert.int_to_bytes_le(x, 8)

# Serializes a transaction to its bytes representation
def serialize(txobj):
    o = bytearray()

    o += convert.int_to_bytes_le(txobj["version"], 4)
    o += encode_var_int(len(txobj["ins"]))
    for inp in txobj["ins"]:
        o += inp["outpoint"]["hash"][::-1]
        o += convert.int_to_bytes_le(inp["outpoint"]["index"], 4)
        o += encode_var_int(len(inp["script"])) + inp["script"]
        o += convert.int_to_bytes_le(inp["sequence"], 4)
    o += encode_var_int(len(txobj["outs"]))
    for out in txobj["outs"]:
        o += convert.int_to_bytes_le(out["value"], 8)
        o += encode_var_int(len(out["script"])) + out["script"]
    o += convert.int_to_bytes_le(txobj["locktime"], 4)

    return bytes(o)

SIGHASH_ALL = 1
SIGHASH_NONE = 2
SIGHASH_SINGLE = 3
SIGHASH_ANYONECANPAY = 0x80

def sighash(tx, i, prevScript, hashtype = SIGHASH_ALL):
    assert isinstance(tx, dict)
    i = int(i)

    newtx = copy.deepcopy(tx)
    for inp in newtx["ins"]:
        inp["script"] = b''

    s = script.deserialize(prevScript)
    s = [x for x in s if x is not script.Opcode.OP_CODESEPARATOR]
    newtx["ins"][i]["script"] = script.serialize(s)

    if hashtype & 0x1f == SIGHASH_NONE:
        newtx["outs"] = []
        for inp in range(len(newtx['ins'])):
            if inp != i:
                newtx['ins'][inp]['sequence'] = 0
    elif hashtype & 0x1f == SIGHASH_SINGLE:
        newtx["outs"] = newtx["outs"][:i+1]
        for out in range(i):
            newtx["outs"][out]['value'] = 2**64 - 1
            newtx["outs"][out]['script'] = b''
        for inp in range(len(newtx['ins'])):
            if inp != i:
                newtx['ins'][inp]['sequence'] = 0

    if hashtype & SIGHASH_ANYONECANPAY != 0:
        newtx["ins"] = [newtx["ins"][i]]

    hashbytes = convert.int_to_bytes_le(hashtype, 4)
    return hashes.hash256(serialize(newtx) + hashbytes)

# Signs a transaction input that spends a p2pk output
# tx: the transaction to sign. It will be modified in place.
# i: the index of the input to sign
# priv: private key, non serialized.
# pub: public key, serialized. Must be correctly encoded as compressed or uncompressed
# HashType: Specifies what parts of the tx to include when signing it.
def sign_p2pk(tx, i, priv, pub, hashtype = SIGHASH_ALL):
    assert isinstance(tx, dict)
    i = int(i)
    assert isinstance(priv, int)
    assert isinstance(pub, bytes)

    prev_script = script.make_p2pk(pub)
    txhash = sighash(tx, i, prev_script, hashtype)
    sig = ecdsa.sign(txhash, priv)
    sig = ecdsa.serialize_sig(sig) + convert.int_to_byte(hashtype)
    tx["ins"][i]["script"] = script.serialize([sig])


# Signs a transaction input that spends a p2pkh output
# tx: the transaction to sign. It will be modified in place.
# i: the index of the input to sign
# priv: private key, non serialized.
# pub: public key, serialized. Must be correctly encoded as compressed or uncompressed
# HashType: Specifies what parts of the tx to include when signing it.
def sign_p2pkh(tx, i, priv, pub, hashtype = SIGHASH_ALL):
    assert isinstance(tx, dict)
    i = int(i)
    assert isinstance(priv, int)
    assert isinstance(pub, bytes)

    address = hashes.hash160(pub)
    prev_script = script.make_p2pkh(address)
    txhash = sighash(tx, i, prev_script, hashtype)
    sig = ecdsa.sign(txhash, priv)
    sig = ecdsa.serialize_sig(sig) + convert.int_to_byte(hashtype)
    tx["ins"][i]["script"] = script.serialize([sig, pub])

# Signs a transaction input that spends a multisig output
# tx: the transaction to sign. It will be modified in place.
# i: the index of the input to sign
# prev_script: Serialized scriptPubKey of the previous output.
# privs: private keys, non serialized.
# pubs: public keys, serialized. Must be correctly encoded as compressed or uncompressed
# HashType: Specifies what parts of the tx to include when signing it.
def sign_multisig(tx, i, prev_script, privs, pubs, hashtype = SIGHASH_ALL):
    assert isinstance(tx, dict)
    i = int(i)
    assert len(privs) == len(pubs)

    txhash = sighash(tx, i, prev_script, hashtype)

    s = [
        script.Opcode.OP_0,
    ]

    for j in range(len(privs)):
        priv = privs[j]
        pub = pubs[j]
        sig = ecdsa.sign(txhash, priv)
        sig = ecdsa.serialize_sig(sig) + convert.int_to_byte(hashtype)
        s.append(sig)

    tx["ins"][i]["script"] = script.serialize(s)

def txhash(tx):
    return hashes.hash256(tx)[::-1]
