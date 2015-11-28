from __future__ import absolute_import, unicode_literals
import os

import mock

from django.test import TestCase
from django.utils.encoding import force_text

from dj_oydiv.utils.random import random_ascii_letters
from dj_oydiv.models import VidyoAdmin
from dj_oydiv.utils.crypto import (
    sym_encrypt_cfb_128,
    sym_decrypt_cfb_dict
)
from . import PACKAGE_BASE
from .models import (
    CryptoTextTest,
    save_then_retrieve,
)


class TestCryptoTextTests(TestCase):
    """
    The test in this class validate basic sanity of the crypto object.
    These tests include sanity-checking/data verification that the data stored
    looks *somewhat* encrypted. They're mostly just functionality tests, and
    assertions that bad input results in errors as we're relying on the sanity
    on pyCrypto
    """
    cleartext = 'aaaaaaaaaaaaaaaaaa'
    key = 'password'
    badkey = 'wrong!'
    newkey = 'anothertotallysecretpassword'

    def test_no_cleartext_saved(self):
        t = CryptoTextTest()
        t.key = self.key
        t.data = self.cleartext
        t.save()
        pk = t.pk
        t = CryptoTextTest.objects.get(pk=pk)
        t.key = self.key
        self.assertNotEqual(t.ciphertext, self.cleartext)
        self.assertNotIn(self.cleartext, t.ciphertext)

    def test_change_key(self):
        t = CryptoTextTest()
        t.key = self.key
        t.data = self.cleartext
        t = save_then_retrieve(t, key=self.key)
        t.change_key(self.newkey)
        t = save_then_retrieve(t, key=self.newkey)
        self.assertEqual(self.cleartext, t.data)

    def test_data_property(self):
        t = CryptoTextTest()
        t.key = self.key
        t.data = self.cleartext
        self.assertNotEqual(t.data, t.ciphertext)
        old_ciphertext = t.ciphertext
        t.data = self.cleartext + self.cleartext
        self.assertNotEqual(old_ciphertext, t.ciphertext)

    def test_empty_key_fails(self):
        with self.assertRaises(ValueError):
            CryptoTextTest(data=self.cleartext, key='')

    def test_db_manager_search_with_kwargs_key(self):
        pass

    def test_verify_returned_data_equal(self):
        t = CryptoTextTest()
        t.key = self.key
        t.data = self.cleartext
        t = save_then_retrieve(t, key=self.key)
        self.assertEqual(self.cleartext, t.data)

    def test_bad_password_fails(self):
        t = CryptoTextTest()
        t.key = self.key
        t.data = self.cleartext

        with self.assertRaises(ValueError):
            t = CryptoTextTest()
            t.key = self.key
            t.data = self.cleartext
            save_then_retrieve(t, key=self.badkey).data

    def test_tamper_evident(self):
        """change a digit of the hmac_digest, and assert that decryption fails with ValueError"""
        t = CryptoTextTest()
        t.key = self.key
        t.data = self.cleartext
        t = save_then_retrieve(t, key=self.key)
        scheme, iv, kdf_iter, kdf_salt, hmac_algo, hmac_hex, \
            ciphertext = t.ciphertext.split("$")

        l = int(hmac_hex, base=16)
        #convert the hmac to int, add 1, and convert back to hex
        hmac_hex = hex(l + 1)[2:-1]
        t.ciphertext = '$'.join((
            scheme, iv, kdf_iter, kdf_salt,
            hmac_algo, hmac_hex, ciphertext)
        )
        with self.assertRaises(ValueError):
            t.data

    def test_large_binary_data(self):
        """
        We're using a text field and require the ability to store large amount of binary data.
        """
        data = os.urandom(2 ** 20)
        t = CryptoTextTest(data=data, key=self.key)
        t = save_then_retrieve(t, key=self.key)
        self.assertEqual(t._decrypt(self.key), data)

    def test_same_params_different_outputs(self):
        """Verify we're using unique values for salt"""
        t1 = CryptoTextTest(data=self.cleartext, key=self.key)
        t2 = CryptoTextTest(data=self.cleartext, key=self.key)
        t1 = save_then_retrieve(t1, key=self.key)
        t2 = save_then_retrieve(t2, key=self.key)
        self.assertNotEqual(t1.ciphertext, t2.ciphertext)

    def test_crypto_roundtrip(self):
        t = CryptoTextTest()
        t.key = self.key
        t.data = self.cleartext
        t = save_then_retrieve(t, key=self.key)
        self.assertEqual(self.cleartext, t.data)


class TestMultipleCrypto(TestCase):
    """
    User objects delegate the responsiblity for handling re-keying to the assigned admin
    objects.
    Tests here check that Admin key-rotation works
    """
    def test_it_please(self):
        # XXX Refactor this into an actual test.
        for admin in [VidyoAdmin(portal_user=str(1 + x)) for x in range(1)]:
            admin.set_password('mypassword', 'mysecretdata')
            admin.save()


class TestRandomAsciiLetters(TestCase):

    ascii_printable = ''.join(chr(x) for x in range(0x20, 0x7f, 1))

    def test_issue81_regression(self):
        """We switched to django.utils.crypto.get_random_string() because we were
        generating passwords with the builtin mersenne twister, seeded manually
        from '/dev/urandom'.
        This had already been 'fixed' once due to missing parens in a seed() call.
        This regression test ensures that we're using django's sane, portable
        crypto-quality generator, instead of some unvetted pile.
        """
        with mock.patch(
            PACKAGE_BASE + '.utils.random.get_random_string',
            mock.MagicMock(return_value='thisisrandom')
        ) as patched:
            string = random_ascii_letters()
            self.assertEqual(string, 'thisisrandom')
            self.assertTrue(patched.called)

    def test_ascii_only(self):
        for x in range(1000):
            s = random_ascii_letters()
            for c in s:
                self.assertIn(c, self.ascii_printable)

    def test_multiple_iterations_nequal(self):
        """Totally naive basic randomness check.
        (the implementation uses django.utils.crypto.get_random_string()
        under the hood so this should suffice)
        """
        s1 = random_ascii_letters()
        s2 = random_ascii_letters()
        self.assertNotEqual(s1, s2)

    def test_crypto_dict_roundtrip(self):
        crypt = sym_encrypt_cfb_128('secret', 'sauce')
        self.assertEqual(force_text(sym_decrypt_cfb_dict('secret', crypt)), 'sauce')


class CryptoBackwardCompatibilityTests(TestCase):
    """
    We want the ability to add/remove dependencies as needed for speed, platform
    availability or similiar.
    However, data in production databases should still be valid.
    Test these fixtures decrypt to the expected values.
    A new feature, primitive or significant change should add a
    backwards compatibility test here
    """
    def test_backward_compatibility_sym_decrypt_cfb_128(self):
        # sym_encrypt_cfb_128('secret', 'something nobody knows') git@f6688dde6
        crypt = {
            'aes_iv_64': b'azm8m1zKYDQ/uuCGzqxMGA==',
            'ciphertext_64': b'1n3rGiH4AXBQyz4EGT6+0ruhf3ev9A==',
            'hmac_algo': 'sha256',
            'hmac_hex': 'ef849dedefc26b45c1d13cd50de5487159f9af9fccf987318217491f47287588',
            'kdf_algo': 'PBKDF2',
            'kdf_iter': 1,
            'kdf_salt_64': b'J0E0RKe0r+w='
        }
        self.assertEqual(
            force_text(sym_decrypt_cfb_dict('secret', crypt)),
            'something nobody knows'
        )
