from . import CredkeepTestCase
from credkeep.util import clear_to_enc_filename, enc_to_clear_filename, CredkeepException


class TestClearToEnc(CredkeepTestCase):
    def test_basic(self):
        enc_fname = 'filename.enc.json'
        clear_fname = 'filename.json'
        self.create_temp(enc_fname)

        found_fname = clear_to_enc_filename(clear_fname)
        self.assertIsInstance(found_fname, str)
        self.assertEqual(found_fname, enc_fname)

    def test_wrong_type(self):
        # files should be json
        fname = 'filename.txt'
        self.create_temp(fname)
        with self.assertRaises(CredkeepException):
            clear_to_enc_filename(fname)

    def test_not_exists(self):
        found_fname = clear_to_enc_filename('filename.json')
        self.assertEqual(found_fname, None)

    def test_already_enc(self):
        # filenames should not have .enc
        with self.assertRaises(CredkeepException):
            clear_to_enc_filename('filename.enc.json')


class TestEncToClear(CredkeepTestCase):
    def test_basic(self):
        enc_fname = 'filename.enc.json'
        clear_fname = 'filename.json'
        self.create_temp(clear_fname)

        found_fname = enc_to_clear_filename(enc_fname)
        self.assertIsInstance(found_fname, str)
        self.assertEqual(found_fname, clear_fname)

    def test_wrong_type(self):
        # files should be json
        fname = 'filename.txt'
        self.create_temp(fname)
        with self.assertRaises(CredkeepException):
            enc_to_clear_filename(fname)

    def test_not_exists(self):
        found_fname = enc_to_clear_filename('filename.enc.json')
        self.assertEqual(found_fname, None)

    def test_already_clear(self):
        # filenames should have .enc
        with self.assertRaises(CredkeepException):
            enc_to_clear_filename('filename.json')
