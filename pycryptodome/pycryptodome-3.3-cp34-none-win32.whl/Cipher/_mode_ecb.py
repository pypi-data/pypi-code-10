# -*- coding: utf-8 -*-
#
#  Cipher/mode_ecb.py : ECB mode
#
# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# No rights are reserved.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===================================================================

"""
Electronic Code Book (ECB) mode.
"""

__all__ = [ 'EcbMode' ]

from Crypto.Util._raw_api import (load_pycryptodome_raw_lib,
                                  VoidPointer, create_string_buffer,
                                  get_raw_buffer, SmartPointer,
                                  c_size_t, expect_byte_string)

raw_ecb_lib = load_pycryptodome_raw_lib("Crypto.Cipher._raw_ecb", """
                    int ECB_start_operation(void *cipher,
                                            void **pResult);
                    int ECB_encrypt(void *ecbState,
                                    const uint8_t *in,
                                    uint8_t *out,
                                    size_t data_len);
                    int ECB_decrypt(void *ecbState,
                                    const uint8_t *in,
                                    uint8_t *out,
                                    size_t data_len);
                    int ECB_stop_operation(void *state);
                    """
                                        )


class EcbMode(object):
    """*Electronic Code Book (ECB)*.

    This is the simplest encryption mode. Each of the plaintext blocks
    is directly encrypted into a ciphertext block, independently of
    any other block.

    This mode is dangerous because it exposes frequency of symbols
    in your plaintext. Other modes (e.g. *CBC*) should be used instead.

    See `NIST SP800-38A`_ , Section 6.1.

    .. _`NIST SP800-38A` : http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf
    """

    def __init__(self, block_cipher):
        """Create a new block cipher, configured in ECB mode.

        :Parameters:
          block_cipher : C pointer
            A smart pointer to the low-level block cipher instance.
        """

        self._state = VoidPointer()
        result = raw_ecb_lib.ECB_start_operation(block_cipher.get(),
                                                 self._state.address_of())
        if result:
            raise ValueError("Error %d while instatiating the ECB mode"
                             % result)

        # Ensure that object disposal of this Python object will (eventually)
        # free the memory allocated by the raw library for the cipher
        # mode
        self._state = SmartPointer(self._state.get(),
                                   raw_ecb_lib.ECB_stop_operation)

        # Memory allocated for the underlying block cipher is now owned
        # by the cipher mode
        block_cipher.release()

    def encrypt(self, plaintext):
        """Encrypt data with the key set at initialization.

        The data to encrypt can be broken up in two or
        more pieces and `encrypt` can be called multiple times.

        That is, the statement:

            >>> c.encrypt(a) + c.encrypt(b)

        is equivalent to:

             >>> c.encrypt(a+b)

        This function does not add any padding to the plaintext.

        :Parameters:
          plaintext : byte string
            The piece of data to encrypt.
            The length must be multiple of the cipher block length.
        :Return:
            the encrypted data, as a byte string.
            It is as long as *plaintext*.
        """

        expect_byte_string(plaintext)
        ciphertext = create_string_buffer(len(plaintext))
        result = raw_ecb_lib.ECB_encrypt(self._state.get(),
                                         plaintext,
                                         ciphertext,
                                         c_size_t(len(plaintext)))
        if result:
            raise ValueError("Error %d while encrypting in ECB mode" % result)
        return get_raw_buffer(ciphertext)

    def decrypt(self, ciphertext):
        """Decrypt data with the key set at initialization.

        The data to decrypt can be broken up in two or
        more pieces and `decrypt` can be called multiple times.

        That is, the statement:

            >>> c.decrypt(a) + c.decrypt(b)

        is equivalent to:

             >>> c.decrypt(a+b)

        This function does not remove any padding from the plaintext.

        :Parameters:
          ciphertext : byte string
            The piece of data to decrypt.
            The length must be multiple of the cipher block length.

        :Return:
            the decrypted data (byte string).
            It is as long as *ciphertext*.
        """

        expect_byte_string(ciphertext)
        plaintext = create_string_buffer(len(ciphertext))
        result = raw_ecb_lib.ECB_decrypt(self._state.get(),
                                         ciphertext,
                                         plaintext,
                                         c_size_t(len(ciphertext)))
        if result:
            raise ValueError("Error %d while decrypting in ECB mode" % result)
        return get_raw_buffer(plaintext)


def _create_ecb_cipher(factory, **kwargs):
    """Instantiate a cipher object that performs ECB encryption/decryption.

    :Parameters:
      factory : module
        The underlying block cipher, a module from ``Crypto.Cipher``.

    All keywords are passed to the underlying block cipher.
    See the relevant documentation for details (at least ``key`` will need
    to be present"""

    cipher_state = factory._create_base_cipher(kwargs)
    if kwargs:
        raise ValueError("Unknown parameters for ECB: %s" % str(kwargs))
    return EcbMode(cipher_state)
