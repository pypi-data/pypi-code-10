__author__ = 'gkhunger'

import filecmp
import os
import json
import time

import validators
import pytest
import requests

import ncryptify.client as ncryptify
import ncryptify.config as config
import ncryptify.ncryptify_exceptions as Exceptions
import uuid


NODE_ENCRYPTED_BLOB = "740000001076657273696f6e000100000002616c676f726974686d000e00000069642d6165733235362d47434d00026b65794964002500000039626363626364302d616164632d343330662d616564662d32336331653438316238323200056976000c00000000339fba53ba7e4c213d56025200d213e9bb0f95564fc8daeae76f978d5520fbb51c9f4e8d763d353b76ee0936e1826a7361f3f7ff4bd2f1537d38a1e27a"
NODE_ENCRYPTED_ID = "3ee1f89e-6340-4123-91d7-a39eee330586"
NODE_ENCRYPTED_SECRET = "H1XVC90Uewd3U9WUUVt9mNCAAZYbi5cgR19OZlpS7cn2fAfQvZYRbCTbP5mzqpb3"
NODE_ENCRYPTED_ISSUER = "https://formfillastic.fitzysoft.com"
NODE_ENCRYPTED_SUBJECT = "NODEJS-BLOB-KAT1-subject"

client = ncryptify.Client.init_with_client_id(os.environ['NCRYPTIFY_ID'],
                                              os.environ['NCRYPTIFY_SECRET'],
                                              'myapp', 5, 'someone@myapp')

# fpe_key = "FPEKeyForTestingUsage"


def make_key_name():
    return "not-a-uuid-" + str(uuid.uuid4())


def find_or_generate_fpe_key(token, name):
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
    url = config.NCRYPTIFY_URL + "/vault/keys"
    key_data = {
        'name': name,
        'usage': "fpe"
    }
    requests.post(url, headers=headers, data=json.dumps(key_data))
    # # Create an FPE.
    # find_or_generate_fpe_key(client.get_token(), fpe_key)


def test_hide_with_invalid_token():
    test_client = ncryptify.Client.init_with_client_id('adummyid',
                                                       'ZHVtbXkgZGF0YQ==',
                                                       'TEST_ISSUER', 5, 'test_subject')
    res = test_client.hide("test", "testKey", "alphabet")
    assert 'Unauthorized' in res


def test_hide_unhide():
    pt = "test"
    ct = client.hide(pt, "testFpeKey", "alphabet")
    dt = client.unhide(ct, "testFpeKey", "alphabet")
    assert ct is not None and dt is not None
    assert pt != ct
    assert pt == dt


def test_get_key():
    key_name = "test_Key"
    key = client.get_key(key_name)
    key_attr = ['account', 'devAccount', 'application', 'name', 'material', 'uri', 'meta', 'updatedAt', 'id',
                'createdAt', 'usage']
    key_attr.sort()
    assert (key['name'] == key_name)
    actualProps = [prop for prop in key]
    actualProps.sort()
    assert key_attr == actualProps


def test_get_random():
    random = client.get_random(16)
    assert len(random) == 16


def test_delete_existing_key():
    key_name = "dummyKeyForDeleting"
    client.get_key(key_name)
    res = client.delete_key(key_name)
    assert (res == 'Key Deleted Successfully')


def test_blob_encryption_without_blob_key():
    fpe_key = make_key_name()
    find_or_generate_fpe_key(client.get_token(), fpe_key)
    with pytest.raises(Exceptions.ErrorFetchingKey):
        client.hide("test", fpe_key, "blob")


def test_delete_non_existent_key():
    key_name = "aNonExistentKey"
    with pytest.raises(Exceptions.KeyNotDeleted):
        client.delete_key(key_name)


def test_hide_unhide_blob():
    ct = client.hide("test string for NODEJS-BLOB-KAT1", "blob_Key", "blob")
    assert client.unhide(ct, "blob_Key", "blob") == "test string for NODEJS-BLOB-KAT1"


def test_decrypt_node_encrypted_blob():
    test_client = ncryptify.Client.init_with_client_id(os.environ['NCRYPTIFY_ID'],
                                                       os.environ['NCRYPTIFY_SECRET'],
                                                       'https://formfillastic.fitzysoft.com', 5,
                                                       'NODEJS-BLOB-KAT1-subject')
    pt = test_client.unhide(NODE_ENCRYPTED_BLOB, None, "blob")
    assert pt == "test string for NODEJS-BLOB-KAT1"


def test_encrypt_file_with_fpe_key():
    fpe_key = make_key_name()
    find_or_generate_fpe_key(client.get_token(), fpe_key)
    path = "test/"
    filename = "testfile-small.txt"
    plain_text_filename = path + filename
    encrypted_text_filename = path + 'encrypted_' + filename

    open(encrypted_text_filename, 'w+')
    with pytest.raises(Exceptions.ErrorFetchingKey):
        client.encrypt_file(fpe_key, plain_text_filename, encrypted_text_filename)


def test_encrypt_decrypt_file():
    def test_encrypt_decrypt_file_helper(filename):
        path = "test/"
        plain_text_filename = path + filename
        encrypted_text_filename = path + 'encrypted_' + filename
        decrypted_text_filename = path + 'decrypted_' + filename

        open(encrypted_text_filename, 'w+')
        open(decrypted_text_filename, 'w+')
        client.encrypt_file("blob_Key", plain_text_filename, encrypted_text_filename)
        client.decrypt_file(encrypted_text_filename, decrypted_text_filename)
        assert filecmp.cmp(plain_text_filename, decrypted_text_filename)
        os.remove(encrypted_text_filename)
        os.remove(decrypted_text_filename)

    test_encrypt_decrypt_file_helper('testfile-small.txt')
    test_encrypt_decrypt_file_helper('testfile-large.txt')
    test_encrypt_decrypt_file_helper('testfile-16.txt')
    test_encrypt_decrypt_file_helper('testfile-32.txt')
    test_encrypt_decrypt_file_helper('testfile-64.txt')
    test_encrypt_decrypt_file_helper('testfile-big.pdf')


def test_decrypt_node_encrypted_file():
    path = "test/"
    plain_text_filename = path + "testfile-small.txt"
    encrypted_text_filename = path + "node_encrypted_testfile.txt"
    decrypted_text_filename = path + "decrypted_node_encrypted_testfile.txt"

    open(encrypted_text_filename, 'w+')
    open(decrypted_text_filename, 'w+')
    client.encrypt_file("blob_Key", plain_text_filename, encrypted_text_filename)
    client.decrypt_file(encrypted_text_filename, decrypted_text_filename)
    assert filecmp.cmp(plain_text_filename, decrypted_text_filename)
    os.remove(decrypted_text_filename)


def test_get_account():
    account = client.get_account()
    assert account is not None
    assert account['id'] is not None
    assert account['id'].strip() != ""


def test_get_link_url():
    url = client.get_link_url("http://fictitiousurl.com/cb")
    assert url is not None
    val = validators.url(url)
    assert val is True


def test_init_with_jwt():
    token = ncryptify.Client.construct_jwt(NODE_ENCRYPTED_ID, NODE_ENCRYPTED_SECRET, NODE_ENCRYPTED_ISSUER, 5,
                                           NODE_ENCRYPTED_SUBJECT)
    test_client = ncryptify.Client.init_with_jwt(token)
    pt = test_client.unhide(NODE_ENCRYPTED_BLOB, "nodeBlobKey", "blob")
    assert pt == "test string for NODEJS-BLOB-KAT1"


# todo: put these back but see if we can make them run without a big ass sleep

def test_token_renewal():
    test_client = ncryptify.Client.init_with_client_id(os.environ['NCRYPTIFY_ID'], os.environ['NCRYPTIFY_SECRET'],
                                                       'myapp', -1, 'someone@myapp')
    #time.sleep(100)
    assert test_client.hide("test", "testFpeKey", "alphabet") != "test"


def test_fail_token_renewal():
    token = ncryptify.Client.construct_jwt(os.environ['NCRYPTIFY_ID'], os.environ['NCRYPTIFY_SECRET'],
                                           'https://formfillastic.fitzysoft.com', -1, 'NODEJS-BLOB-KAT1-subject')
    test_client = ncryptify.Client.init_with_jwt(token)
    failed = False
    try:
        test_client.unhide(NODE_ENCRYPTED_BLOB, "nodeBlobKey", "blob")
    except Exception as e:
        assert e.message == 'Key Not Found'
        failed = True
    assert failed

