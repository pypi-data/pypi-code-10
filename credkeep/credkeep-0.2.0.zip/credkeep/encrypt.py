import base64
import json
from .util import kms, default_keyname


def encrypt_secret(secret, key=default_keyname):
    resp = kms.encrypt(KeyId=key, Plaintext=base64.b64encode(secret))
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
    return base64.b64encode(resp['CiphertextBlob'])


def encrypt_file(filename, output_filename=None, key=default_keyname):
    data = json.load(open(filename))
    results = {}

    for k, v in data.iteritems():
        v_encrypt = encrypt_secret(v, key=key)
        results[k] = v_encrypt

    if output_filename:
        json.dump(results, open(output_filename, 'w'), indent=2)
    else:
        print json.dumps(results, indent=2)
    return results
