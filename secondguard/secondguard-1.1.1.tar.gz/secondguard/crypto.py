# PyCrypto AES Library
from Crypto.Cipher import AES

# Base 64 encoding for DB storage as text string
from base64 import standard_b64encode, standard_b64decode

# Randomness source for cipher
from os import urandom


def is_128_bits(text):
    '''
    Returns a list of the following form:

        (bool, 'err_msg')
    '''
    if type(text) in (str, bytes, unicode):
        if len(text) == 16:
            return True, ''
        else:
            return False, 'Text `%s` is not 16 chars (128 bits)' % text
    else:
        return False, 'Text `%s` is `%s` not a string or bytes' % (text, type(text))


def assert_was_aescfb_encrypted(text):
    base_err = 'This string not originally encrypted with AES CFB using this module'
    if not text.startswith('SG-AESCFB-v1$'):
        raise Exception(base_err + ' (it would start with `SG-AESCFB-v1$`)')
    if not text.count('$') == 2:
        raise Exception(base_err + ' (it would have 2 $s)')
    if not text.find('@') > 33:
        raise Exception(base_err + ' (it would have a @ to delimit seed from nonce and iv from ciphertext)')


def encrypt(secret_message, key, iv=None):
    '''
    Easy to use method for encrypting data client-side.
    No crypto knowledge needed.

    Encrypt `secret_message` (can be of $encoding `bytes` or `string`) with a
    128 bit key.

    You can supply a given 128 bit IV, or if `None` is supplied (default) then
    a random 128 bit IV will be generated.

    Uses AES in CFB mode.

    Base64 encode the result and convert to utf-8 for storage.

    The final result will look like this ($ delimited without spaces):

        SG-AESCFB-v1 $encoding $b64iv@b64ciphtertext

    '''
    # `secret_message` could be a binary object (say a file) or a string
    # need to store this to determine encoding to return when calling `decrypt`
    if type(secret_message) is bytes:
        encoding = 'bytes'
    elif type(secret_message) is str:
        encoding = 'string'
    elif type(secret_message) is unicode:
        encoding = 'unicode'
    else:
        raise Exception('`secret_message` must be of type (bytes, str, unicode), not %s' % type(secret_message))

    if iv:
        is_128, err_msg = is_128_bits(text=iv)
        if not is_128:
            raise Exception('Invalid IV `%s`: %s' % (iv, err_msg))
    else:
        iv = urandom(16)[:16]
        is_128, err_msg = is_128_bits(text=iv)
        if not is_128:
            raise Exception('Invalid IV Generated `%s`: %s' % (iv, err_msg))

    is_128, err_msg = is_128_bits(text=key)
    if not is_128:
        raise Exception('Invalid Key `%s`: %s' % (key, err_msg))

    cipher = AES.new(key, AES.MODE_CFB, iv)
    ciphertext_in_bytes = cipher.encrypt(secret_message)

    b64_text_to_decrypt = 'SG-AESCFB-v1$%s$%s@%s' % (
            encoding,
            standard_b64encode(iv).decode('utf-8'),
            standard_b64encode(ciphertext_in_bytes).decode('utf-8'),
            )

    # redundant defensive check
    assert_was_aescfb_encrypted(b64_text_to_decrypt)

    return b64_text_to_decrypt


def decrypt(b64_text_to_decrypt, key):
    '''
    Reverses the operation performed in `encrypt`.

    Be sure to supply your key in the same format as before (as bytes and not a string).

    Remember that when you decrypt, you will return secret_message in bytes (as you originally supplied it).
    If you want it as a string, you'll have to convert it:

        result_after_decrypting.decode('utf-8')

    '''
    assert_was_aescfb_encrypted(b64_text_to_decrypt)
    is_128, err_msg = is_128_bits(text=key)
    if not is_128:
        raise Exception('Invalid Key `%s`: %s' % (key, err_msg))

    _, encoding, b64_iv_and_ciphertext = b64_text_to_decrypt.split('$')
    iv_b64_string, ciphertext_b64_string = b64_iv_and_ciphertext.split('@')

    ciphertext_in_bytes = standard_b64decode(ciphertext_b64_string.encode('utf-8'))

    iv_in_bytes = standard_b64decode(iv_b64_string.encode('utf-8'))
    is_128, err_msg = is_128_bits(text=iv_in_bytes)
    if not is_128:
        raise Exception('Invalid IV `%s`: %s' % (iv_in_bytes, err_msg))

    cipher = AES.new(key, AES.MODE_CFB, iv_in_bytes)
    plaintext = cipher.decrypt(ciphertext_in_bytes)

    if encoding == 'bytes':
        return plaintext
    elif encoding == 'string':
        return plaintext.decode('utf-8')
    elif encoding == 'unicode':
        return plaintext.encode('utf-8')
    else:
        raise Exception('Unknown Encoding: %s' % encoding)
