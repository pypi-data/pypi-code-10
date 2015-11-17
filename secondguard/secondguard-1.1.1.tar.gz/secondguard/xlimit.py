# API
from secondguard import get_encryption_info, get_decryption_info

# Utility Functions
from secondguard.utils import is_valid_seed_hex, is_seed_hash_pair, derive_child_key

# Crypto
from secondguard.crypto import encrypt, decrypt


KEY_LENGTH_IN_BYTES = 16


def was_aescfb_sg_encrypted(text):
    base_err = 'This string not originally encrypted with AES CFB using SG and this module'
    if not text.startswith('SG-AESCFB-v1$'):
        return False, base_err + ' (it would start with `SG-AESCFB-v1$`)'
    if not text.count('$') == 5:
        return False, base_err + ' (it would have 5 $s)'


def assert_was_aescfb_encrypted(text):
    was_encrypted, err_msg = was_aescfb_sg_encrypted(text=text)
    if not was_encrypted:
        raise Exception(err_msg)


def sg_encrypt_secret(secret_to_encrypt, seed_pub_hash_hex, sg_api_token):
    '''
    Encrypt a list of secrets_to_encrypt using a unique key from secondguard for each one

    Must supply an sg_api_token and seed_pub_hash_hex to use.
    '''
    return sg_batch_encrypt_secrets(
            secrets_to_encrypt=[secret_to_encrypt, ],
            seed_pub_hash_hex=seed_pub_hash_hex,
            sg_api_token=sg_api_token,
            )[0]


def sg_batch_encrypt_secrets(secrets_to_encrypt, seed_pub_hash_hex, sg_api_token):
    '''
    Batch method for sg_encrypt_secret

    Local encryption takes longer the longer your data to encrypt is.

    If you're encrypting a large document, batching will not really
    speed up the whole process (and complicates your code).

    If you're encrypting lots of small data points (say SSNs), then batching
    your API calls in groups of 5-500 can have large performance increases.
    '''

    assert sg_api_token, 'sg_api_token required'
    is_valid, err_msg = is_valid_seed_hex(seed_pub_hash_hex)
    if not is_valid:
        raise Exception('Invalid `seed_pub_hash_hex`: %s' % err_msg)

    assert type(secrets_to_encrypt) in (list, tuple), "secrets_to_encrypt must be a list or tuple"
    assert len(secrets_to_encrypt) < 1000, "Max of 1000 secrets to encrypt"

    api_response = get_encryption_info(
            seed_pub_hash=seed_pub_hash_hex,
            api_token=sg_api_token,
            num_keys=len(secrets_to_encrypt),
            version='v1',
            )

    if 'error' in api_response:
        raise Exception(api_response['error'])
    if 'errors' in api_response:
        raise Exception(api_response['errors'])

    to_store_list = []
    for cnt, obj in enumerate(api_response):
        seed_and_nonce = '%s@%s' % (seed_pub_hash_hex, obj['nonce'])

        secret_message = secrets_to_encrypt[cnt]

        to_store = encrypt(
                secret_message=secret_message,
                key=obj['key'][:KEY_LENGTH_IN_BYTES],
                iv=None,
                )

        prefix, encoding, b64_iv_and_ciphertext = to_store.split('$')

        # add seed_pub_hash_hex & nonce
        to_store_with_sg_data = '$'.join(
                (
                    prefix,
                    encoding,
                    seed_and_nonce,  # added
                    b64_iv_and_ciphertext,
                    )
                )
        to_store_list.append(to_store_with_sg_data)

    return to_store_list


def sg_decrypt_secret(to_decrypt, api_token):
    '''
    Decypt an item from your database using your api_token.
    '''

    prefix, encoding, seed_and_nonce, b64_iv_and_ciphertext = to_decrypt.split('$')

    seed_pub_hash_hex, nonce = seed_and_nonce.split('@')

    is_valid, err_msg = is_valid_seed_hex(seed_pub_hash_hex)
    if not is_valid:
        raise Exception('Invalid `seed_pub_hash_hex`: %s' % err_msg)

    # TODO: batch these API calls
    api_response = get_decryption_info(
            seed_pub_hash=seed_pub_hash_hex,
            api_token=api_token,
            nonce=nonce,
            version='v1',
            )

    if 'error' in api_response:
        raise Exception(api_response['error'])
    if 'errors' in api_response:
        raise Exception(api_response['errors'])

    key = api_response['key'][:KEY_LENGTH_IN_BYTES]

    b64_text_to_decrypt = '$'.join(
            (
                prefix,
                encoding,
                # no seed_and_nonce
                b64_iv_and_ciphertext
                )
            )

    return decrypt(
            b64_text_to_decrypt=b64_text_to_decrypt,
            key=key,
            )


def sg_decrypt_from_priv_seed(to_decrypt, private_seed_hex):
    '''
    For use with a private seed on your local server.

    WARNING: placing the private seed on your local server defeats the whole
    purpose of rate limiting. If an attacker has access to your encrypted
    database and gets access to this seed on your server, they can easily
    decrypt the whole database. Only use this method if you know what you're
    doing. It's main purpose is recovery in case SecondGuard is down.
    '''
    prefix, encoding, seed_and_nonce_str, b64_iv_and_ciphertext = to_decrypt.split('$')
    seed_pub_hash_hex, nonce = seed_and_nonce_str.split('@')

    valid_pair = is_seed_hash_pair(
            private_seed_hex=private_seed_hex,
            seed_public_hash_hex=seed_pub_hash_hex,
            )
    if not valid_pair:
        err_msg = seed_pub_hash_hex
        err_msg += ' is not a valid private seed for the data you are trying to decrypt.'
        raise Exception(err_msg)

    unique_key = derive_child_key(
            private_seed_hex=private_seed_hex,
            nonce=nonce,
            )

    b64_text_to_decrypt = '$'.join(
            (
                prefix,
                encoding,
                # no seed_and_nonce_str
                b64_iv_and_ciphertext,
                )
            )

    return decrypt(
            b64_text_to_decrypt=b64_text_to_decrypt,
            key=unique_key[:KEY_LENGTH_IN_BYTES],
            )
