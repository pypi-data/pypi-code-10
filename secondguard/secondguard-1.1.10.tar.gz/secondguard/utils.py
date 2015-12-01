from hashlib import sha256
import re

from sys import version_info

HEX_CHARS_RE = re.compile('^[0-9a-f]*$')

ENCRYTPABLE_TYPES = set([bytes, str])
STRING_TYPES = set([str, ])


if version_info.major == 2:
        ENCRYTPABLE_TYPES.add(unicode)
        STRING_TYPES.add(unicode)


def uses_only_hash_chars(string):
    return bool(HEX_CHARS_RE.match(string))


def is_valid_seed_hex(text):
    '''
    Works for both a private_seed_hex and seed_public_hash_hex

    Returns either:

        (True, '')

    Or:

        (False, 'Explanation')

    '''
    if uses_only_hash_chars(text):
        if len(text) == 64:
            return True, ''
        else:
            err_msg = 'text != 64 chars'
            return False, err_msg
    else:
        err_msg = 'text has non-hex characters'
        return False, err_msg


def is_seed_hash_pair(private_seed_hex, seed_public_hash_hex):
    '''
    Confirm that seed_public_hash_hex is the determinstic result of
    of hashing private_seed_hex. Returns a bool.

    This basic check is especially important if you have multiple seeds and
    want to confirm that you're encrypting/decrypting with the correct one.
    '''

    # Defensive checks
    is_valid, err_msg = is_valid_seed_hex(private_seed_hex)
    assert is_valid, 'private_seed_hex error: %s' % err_msg

    is_valid, err_msg = is_valid_seed_hex(seed_public_hash_hex)
    assert is_valid, 'seed_public_hash_hex error: %s' % err_msg

    # The actual code:
    return sha256(private_seed_hex.encode('utf-8')).hexdigest() == seed_public_hash_hex


def derive_child_key(private_seed_hex, nonce):
    '''
    Given a `private_seed_hex` and a `nonce`, return the child key
    as a string in hexadicmal format.
    '''
    # Defensive checks
    is_valid, err_msg = is_valid_seed_hex(private_seed_hex)
    assert is_valid, 'private_seed_hex error: %s' % err_msg

    assert nonce, 'Must supply a nonce'
    err_msg = 'nonce is of type %s and not %s' % (
            type(nonce),
            ','.join([str(x) for x in STRING_TYPES]),
            )
    assert type(nonce) in STRING_TYPES, err_msg

    return sha256((private_seed_hex+nonce).encode('utf-8')).hexdigest()
