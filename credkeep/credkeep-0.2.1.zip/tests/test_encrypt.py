import unittest
import credkeep
import json
import os

# Warning this test class makes actual API calls to the KMS service. Therefore ensure that an boto is configured correctly
class TestEncrypt(unittest.TestCase):
    def test_encrypt(self):
        results = credkeep.encrypt_file('data/test.json', key='alias/test-key')

        self.assertIn('SECRET_API_KEY', results)
        self.assertIn('ANOTHER_API_KEY', results)
        self.assertNotEqual(results['SECRET_API_KEY'], "thisismysecretkey")
        self.assertNotEqual(results['ANOTHER_API_KEY'], "anotherkey")

    def test_output_file(self):
        output = 'data/test_encrypted_temp.json'
        credkeep.encrypt_file('data/test.json', output_filename=output, key='alias/test-key')

        results =json.load(open(output))
        self.assertIn('SECRET_API_KEY', results)
        self.assertIn('ANOTHER_API_KEY', results)
        self.assertNotEqual(results['SECRET_API_KEY'], "thisismysecretkey")
        self.assertNotEqual(results['ANOTHER_API_KEY'], "anotherkey")
        os.remove(output)
