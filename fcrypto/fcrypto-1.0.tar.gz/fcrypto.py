# -*- coding: utf-8 -*-
import os
import base64
import scrypt
import logging

from Crypto              import Random
from Crypto.Cipher       import AES
from Crypto.Hash         import HMAC, SHA256
from Crypto.Protocol.KDF import PBKDF2

# For reference on how to handle IV, HMAC & AES encryption:
# http://crypto.stackexchange.com/questions/11409/how-to-use-hmac-sha1-hmac-sha2-in-conjunction-with-aes

class InvalidBlock(Exception):
    '''Thrown when an encryted block (from a file) cannot be decrypted.'''

    def str(self):
        return 'Invalid block found while decrypting data.'


class FileEncryptorIterator:
    '''File encryptor iterator.

    The iterator is useful if you need to update some status periodically. It
    will encrypt a file block by block, each time returning the number of bytes
    read and the number of bytes written.

    Example:
        from fcrypto import fcrypto
        crypto = fcrypto(...)           # see fcrypto.fcrypto documentation

        with open('...', 'rb') as _if:
            with open('...', 'wb') as _of:
                fc = FileEncryptorIterator(crypto, _if, _of)
                for bytes_read, bytes_written in fc:
                    <do something useful here>
    '''

    _first = True

    def __init__(self, crypto, _if, _of):
        '''Initialize the file encryptor.

        @param crypto the already initialized fcrypto instance to use.
        @param _if the (cleartext) input file handle.
        @param _of the (encrypted) output file handle.
        '''
        assert (crypto.initialized is True)

        self._crypto = crypto
        self._if = _if
        self._of = _of


    def __iter__(self):
        return self


    def __next__(self):
        data_in = self._if.read(self._crypto.bs)
        if len(data_in) == 0:
            self._of.flush()
            raise StopIteration

        prefix = b''
        if self._first:
            prefix += self._crypto._encode_version()

        data_out = self._crypto._encrypt(data_in)
        output_len = self._of.write(prefix + self._crypto._hmac(data_out) + data_out)

        self._first = False

        return (len(data_in), output_len)


class fcrypto:
    '''Small cryptography class to ease the use of python cryptography
       libraries.'''

    CURRENT_VERSION    = 1

    DEFAULT_KEY_ITER   = 1000
    DEFAULT_BLOCK_SIZE = 5*1024*1024    # 5 MB block size for each IV

    _cache = {}

    def __init__(self, passphrase, metadata=None):
        self.passphrase  = passphrase
        self.hmac_size   = None
        self.initialized = False

        self._metadata = self._setup(metadata)
        assert (self.initialized is True)


    def metadata(self):
        '''Return the current cryptographic metadata used for encrypting and
        decrypting data and files.
        
        The format is a dictionary but it's content is opaque to the called. It
        must also be saved as-is by the caller for future decryption.'''
        assert (self.initialized is True)
        return self._metadata


    def hash(self, data):
        '''Return a (deterministic) hash of the input data.'''
        assert (self.initialized is True)
        if type(data) == list:
            return list(map(lambda i: self.hash(i)))
        data = self._as_bytes(data)
        return scrypt.hash(data, self._keys()[2])


    def encrypt(self, data, _version_prefix=True):
        '''Return an encrypted block from the input data.
        
        @param data the cleartext data to encrypt.
        @return the encrypted block, prepended with a random IV and the
                fcrypto version.
        '''
        assert (self.initialized is True)
        data = self._as_bytes(data)
        if type(data) == list:
            return list(map(lambda i: self.encrypt(i)))
        return self._encode_version() + self._encrypt(data)


    def _encrypt(self, data):
        assert (self.initialized is True)
        assert (type(data) == bytes)

        iv = self._iv()
        return iv + self._cipher(iv).encrypt(data)


    def decrypt(self, data, _version_prefix=True):
        '''Return a decrypted block from the input data.
        
        @param data the encrypted block to decrypt.
        @return the cleartext data if successfull, an empty string otherwise.
        '''
        assert (self.initialized is True)
        if type(data) == list:
            return list(map(lambda i: self.decrypt(i)))
        data = self._as_bytes(data)

        version, data = self._decode_version(data)

        methodname = '_decrypt_v{0}'.format(version)
        if not hasattr(self, methodname):
            raise Exception('invalid version #{0}'.format(version))
        return getattr(self, methodname)(data)


    def _decrypt_v1(self, data):
        iv = data[:AES.block_size]
        return self._cipher(iv).decrypt(data[AES.block_size:])


    def encrypt_file(self, _if, _of):
        '''Encrypt a file and place the result in an output file.

        @param _if the (cleartext) input file handle.
        @param _of the (encrypted) output file handle.

        @return (bytes_read, bytes_written) tuple.
        '''
        assert (self.initialized is True)

        bytes_read = 0
        bytes_written = 0

        fc = FileEncryptorIterator(self, _if, _of)
        for br, bw in fc:
            bytes_read += br
            bytes_written += bw

        return (bytes_read, bytes_written)


    def decrypt_file(self, _if, _of):
        '''Decrypt a file and place the result in an output file.

        @param _if the (encrypted) input file handle.
        @param _of the (cleartext) output file handle.
        '''
        assert (self.initialized is True)

        data_in = _if.read(1)
        version_len = int(chr(data_in[0]))
        _if.seek(0)
        data_in = _if.read(1 + version_len)

        version, _ = self._decode_version(data_in)
        methodname = '_decrypt_v{0}'.format(version)
        if not hasattr(self, methodname):
            raise Exception('invalid version #{0}'.format(version))

        data_in = _if.read(self.hmac_size + AES.block_size + self.bs)
        while len(data_in) > 0:
            if data_in[:self.hmac_size] != self._hmac(data_in[self.hmac_size:]):
                raise InvalidBlock()
            data_out = getattr(self, methodname)(data_in[self.hmac_size:])
            _of.write(data_out)
            data_in = _if.read(self.hmac_size + AES.block_size + self.bs)
        _of.flush()


    def _encode_version(self):
        version = bytes(str(self.CURRENT_VERSION).encode('utf-8'))
        return str(len(version)).encode('utf-8') + version


    def _decode_version(self, data):
        assert (type(data) == bytes)
        version_len = int(chr(data[0]))
        return int(data[1:1+version_len].decode('utf-8')), data[1+version_len:]


    def _setup(self, metadata=None):
        assert (self.initialized is False)

        if metadata is not None:
            assert (type(metadata) == dict)

            if metadata['version'] != 1:
                raise InvalidArgument('version', '1')

            if metadata['cipher'] == 'AES':
                self.cipher = AES
            else:
                raise InvalidArgument('cipher', metadata['cipher'])

            if metadata['mode'] == 'CFB':
                self.mode = AES.MODE_CFB
            else:
                raise InvalidArgument('mode', metadata['mode'])

            if metadata['KDF'] != 'PBKDF2':
                raise InvalidArgument('KDF', 'PBKDF2')

            self.salt    = base64.b64decode(metadata['salt'])
            self.bs      = metadata['bs']
            self.keyiter = metadata['keyiter']
            self.version = metadata['version']
        else:
            self.salt    = Random.new().read(AES.block_size)
            self.cipher  = AES
            self.mode    = AES.MODE_CFB
            self.bs      = self.DEFAULT_BLOCK_SIZE
            self.keyiter = self.DEFAULT_KEY_ITER
            self.version = self.CURRENT_VERSION

            metadata = {
                'cipher':  'AES',
                'mode':    'CFB',
                'KDF':     'PBKDF2',
                'salt':    base64.b64encode(self.salt).decode('iso-8859-1'),
                'bs':      self.bs,
                'keyiter': self.keyiter,
                'version': self.version,
            }

        self.hmac_size = HMAC.new(self._keys()[1], digestmod=SHA256).digest_size
        self.initialized = True

        return metadata


    def _hmac(self, data):
        h = HMAC.new(self._keys()[1], digestmod=SHA256)
        h.update(data)
        return h.digest()


    def _keys(self):
        '''Derive three keys from the master passphrase and the random salt.
 
        Key usage:
          - First key: AES cypher key
          - Second key: HMAC key
          - Thrid key: scrypt hash key
        '''
        if 'keys' not in self._cache:
            key_len = 32 - AES.block_size
            keys = PBKDF2(
                self.passphrase,
                self.salt,
                count=self.keyiter,
                dkLen=key_len*3
            )

            self._cache['keys'] = (
                self.salt + keys[:key_len],
                self.salt + keys[key_len:key_len*2],
                self.salt + keys[key_len*2:]
            )
        return self._cache['keys']


    def _cipher(self, iv):
        return AES.new(self._keys()[0], self.mode, iv)


    def _iv(self):
        return Random.new().read(AES.block_size)


    def _as_bytes(self, data):
        if type(data) == bytes:
            return data
        elif type(data) == str:
            try:
                return data.encode('utf-8')
            except UnicodeEncodeError:
                return data.encode('utf-8', 'surrogateescape')
        raise InvalidArgument('data', str(type(data)))
