import base64
import json
import os

from .util import kms, enc_to_clear_filename


def decrypt_secret(secret):
    resp = kms.decrypt(CiphertextBlob=base64.b64decode(secret))
    return base64.b64decode(resp['Plaintext'])


def decrypt_file(filename, set_env=True, override_env=False):
    """
    Decrypts a JSON file containing encrypted secrets. This file should contain an object mapping the key names to
    encrypted secrets. This encrypted file can be created using `credkeep.encrypt_file` or the commandline utility.

    :param filename:  filename of the JSON file
    :param set_env: If True, an environment variable representing the key is created.
    :param override_env: If True, an existing environment variable with the same key name will be overridden with the
        new decrypted value. If False, the environment variable will not be set.
    :return: Dict containing the decrypted keys
    """
    data = json.load(open(filename))

    results = {}

    for key, v in data.iteritems():
        v_decrypt = decrypt_secret(v)

        results[key] = v_decrypt
        if set_env:
            if key in os.environ and not override_env:
                break
            os.environ[str(key)] = v_decrypt

    return results


def decrypt_or_cache(filename, **kwargs):
    """
    Attempts to load a local version of decrypted secrets before making external api calls.

    This is useful as it allows credkeep secrets to be used offline. Options for decrypt_filename can be passed to this
    function.
    :param filename: filename of encrypted JSON file
    :return: Dict containing decrypted keys
    """
    clear_fname = enc_to_clear_filename(filename)
    if clear_fname:
        return json.load(open(clear_fname))

    return decrypt_file(filename, **kwargs)
