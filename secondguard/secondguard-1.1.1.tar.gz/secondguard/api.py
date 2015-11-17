import requests

ENDPOINT = 'https://api.secondguard.com'


def ping(api_token=None):
    r = requests.get(ENDPOINT+'/ping')
    return r.json()


def get_encryption_info(seed_pub_hash, api_token, num_keys=None, version='v1'):
    '''
    Given a `seed_pub_hash` and `api_token` return the following dictionary
    to use in client-side encryption:
      {
        `nonce`: `new_random_nonce`,
        `key`: `key_generated_from_nonce`,
      }

    If you pass a num_keys argument > 1 it will return a list of dictionaries.

    '''
    assert seed_pub_hash, seed_pub_hash
    assert api_token, api_token

    if num_keys:
        assert type(num_keys) is int, num_keys
        assert 0 < num_keys < 1000, num_keys

    assert version == 'v1', version

    params = {
            'token': api_token,
            'seed-pub-hash': seed_pub_hash,
            }

    if num_keys:
        params['num-keys'] = num_keys

    r = requests.get(ENDPOINT + '/encrypt/v1/', params=params)

    return r.json()


def get_decryption_info(seed_pub_hash, api_token, nonce, version='v1'):
    '''
    Given a `seed_pub_hash`, `api_token`, and `nonce`, return the key to use
    in client-side encryption:
      {
        `key`: `key_generated_from_nonce`,
      }
    '''
    assert seed_pub_hash, seed_pub_hash
    assert api_token, api_token
    assert nonce, nonce

    assert version == 'v1', version

    params = {
            'token': api_token,
            'seed-pub-hash': seed_pub_hash,
            'nonce': nonce,
            }

    r = requests.get(ENDPOINT + "/decrypt/v1/", params=params)

    return r.json()
