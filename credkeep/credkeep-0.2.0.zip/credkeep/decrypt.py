import base64
import json
import os

from .util import kms


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
            os.environ[key] = v_decrypt
    return results
