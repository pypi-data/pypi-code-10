import unittest
import credkeep
import json
from . import decrypted_file, encrypted_file


# Warning this test class makes actual API calls to the KMS service. Therefore ensure that an boto is configured correctly
class TestEncrypt(unittest.TestCase):
    def test_encrypt(self):
        results = credkeep.decrypt_file(encrypted_file, set_env=False)

        orig = json.load(open(decrypted_file))

        self.assertDictEqual(orig, results)
