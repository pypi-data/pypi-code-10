from __future__ import absolute_import, unicode_literals

import base64
import hashlib
import hmac
import logging

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from django.utils.encoding import force_bytes

from ..config import config

logger = logging.getLogger(__name__)

ITERATIONS = config.CRYPTO_KDF_ITERATIONS


try:
    constant_time_compare = hashlib.compare_digest
except AttributeError:
    # python < 2.7.9; See [PEP0466](https://www.python.org/dev/peps/pep-0466/)
    from django.utils.crypto import constant_time_compare

try:
    from hashlib import pbkdf2_hmac
    pbkdf2_derive_key = pbkdf2_hmac
    logger.info("Using hashlib.pbkdf2_hmac for key derivation")
except ImportError:
    # python < 2.7.9; See [PEP0466](https://www.python.org/dev/peps/pep-0466/)
    logger.warning("PEP0466 not supported. Falling back to django pbkdf2")
    from django.utils.crypto import pbkdf2

    def pbkdf2_derive_key(hash_name, password, salt, iterations, dklen):
        return pbkdf2(password, salt, iterations, dklen, getattr(hashlib, hash_name))


def sym_encrypt_cfb_128(secret_key, cleartext, hmac_algo='sha256', kdf_iterations=ITERATIONS):
    """perform AES-128 symmetric encryption on an arbitrary cleartext
    using the given secret_key in CFB mode.

    AES-CFB does not require padding the input, so simplifies the task a bit.
    returns a dict of the base64-encoded ciphertext, base64-encoded IV,
    the HMAC-digest-hex, the HMAC-digest-algorithm name,
    the key-derivation function used/number of rounds.
    presently, PBKDF2 is used for key-derivation.

    """
    secret_key = force_bytes(secret_key)
    cleartext = force_bytes(cleartext)
    assert hmac_algo in getattr(
        hashlib,
        'algorithms_available', # See [PEP0466](https://www.python.org/dev/peps/pep-0466/)
        getattr(hashlib, 'algorithms', [])
    )

    # Generate the AES initialisation vector, and the salt used by the key-derivation algo
    salt = get_random_bytes(8)
    iv = get_random_bytes(16)

    # AES-CFB-128 needs a 16byte key.
    # Use PBKDF2 to generate a 16byte key regardless of the secret_key length.
    key = pbkdf2_derive_key('sha1', secret_key, salt, kdf_iterations, 16)

    # we're using AES-128 because Bruce Schneier says not to use 192/256.
    # Who are we to argue?
    # https://www.schneier.com/blog/archives/2009/07/another_new_aes.html#c386957
    crypt = AES.new(key, mode=AES.MODE_CFB, IV=iv)
    ciphertext_64 = base64.b64encode(crypt.encrypt(cleartext))

    # generate the Message Authentication Code according to @hmac_algo
    # The MAC function is passed the cleartext + iv, and password.
    # use the IV to avoid the same cleartext / pw combination giving the same MAC
    hash_fn = getattr(hashlib, hmac_algo)
    h = hmac.new(secret_key, cleartext + iv, hash_fn)

    return {
        'ciphertext_64': ciphertext_64,
        'aes_iv_64': base64.b64encode(iv),
        'kdf_salt_64': base64.b64encode(salt),
        'kdf_algo': 'PBKDF2', # this is currently the only choice
        'kdf_iter': kdf_iterations,
        'hmac_hex': h.hexdigest(),
        'hmac_algo': hmac_algo,
    }


def sym_decrypt_cfb_128(secret_key, ciphertext_64, aes_iv_64,
                        kdf_salt_64, hmac_hex, hmac_algo, kdf_iterations):
    """
    Decrypt an AES-128-CFB ciphertext encypted with sym_decryt_cfb().
    """
    secret_key = force_bytes(secret_key)
    assert hmac_algo in getattr(
        hashlib, 'algorithms_available',
        getattr(hashlib, 'algorithms', [])
    )
    iv = base64.b64decode(aes_iv_64)
    salt = base64.b64decode(kdf_salt_64)
    ciphertext = base64.b64decode(ciphertext_64)

    # derive the original AES 16-byte key in exactly the same way as before
    key = pbkdf2_derive_key('sha1', secret_key, salt, kdf_iterations, 16)
    crypto = AES.new(key, mode=AES.MODE_CFB, IV=iv)

    # decrypt
    cleartext = crypto.decrypt(ciphertext)

    # check that the data has not been tampered with / the password is correct
    hash_fn = getattr(hashlib, hmac_algo)
    mac = hmac.new(secret_key, cleartext + iv, hash_fn)
    if not constant_time_compare(force_bytes(mac.hexdigest()), force_bytes(hmac_hex)):
        raise ValueError("Password incorrect or data corrupt")
    return cleartext


def sym_decrypt_cfb_dict(secret_key, crypto_dict):
    return sym_decrypt_cfb_128(
        secret_key,
        crypto_dict['ciphertext_64'],
        crypto_dict['aes_iv_64'],
        crypto_dict['kdf_salt_64'],
        crypto_dict['hmac_hex'],
        crypto_dict['hmac_algo'],
        crypto_dict['kdf_iter']
    )
