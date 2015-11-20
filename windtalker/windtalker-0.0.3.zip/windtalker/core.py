#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
About
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Copyright (c) 2015 by Sanhe Hu**

- Author: Sanhe Hu
- Email: husanhe@gmail.com
- Lisence: MIT


Compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Python2: Yes
- Python3: Yes
    

Prerequisites
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- cryptography


Class, method, function, exception
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import print_function, unicode_literals
from cryptography.fernet import Fernet
from windtalker.messenger import messenger
import hashlib
import base64
import sys
import os
import io

is_py2 = (sys.version_info[0] == 2)
if is_py2:
    input = raw_input

class SecretKeyNotGivenError(Exception):
    pass

class OverWriteFileError(Exception):
    pass

class PasswordError(Exception):
    pass

class WindTalker():
    """Cipher utility class.
    """
    _secret_key = None
    _encrypt_chunk_size = 1024*1024
    _decrypt_chunk_size = 1398200
    
    def __init__(self):
        pass
    
    def _set_secret_key(self, key):
        """Set your secret key.
        """
        self._secret_key = key
        self.cipher = Fernet(self.any_text_to_fernet_key(key))
        
    @property
    def secret_key(self):
        return self._secret_key
    
    def set_secret_key(self):
        """User command line to enter your secret key.
        """
        self._set_secret_key(input(
            "Please enter your secret key (case sensitive): "))
    
    def set_encrypt_chunk_size(self, chunk_size):
        """Set the size of how much bytes content stored in your memory. Choose 
        it wisely to fit your memory. I recommend use 100MB for large file.
        """
        self._encrypt_chunk_size = chunk_size
        self._decrypt_chunk_size = self.chunk_size_analysis(self._encrypt_chunk_size)
        
    @property
    def encrypt_chunk_size(self):
        return self._encrypt_chunk_size
    
    @property
    def decrypt_chunk_size(self):
        return self._decrypt_chunk_size
    
    def any_text_to_fernet_key(self, text):
        """Generate url_safe base64 encoded key for fernet symmetric encryption.
        """
        m = hashlib.md5()
        m.update(text.encode("utf-8"))
        fernet_key = base64.b64encode(m.hexdigest().encode("utf-8"))
        return fernet_key
    
    def chunk_size_analysis(self, reading_size):
        """Because windtalker working in streaming mode (read/write content by 
        byte block), so we have to match the reading size with its corresponding
        writing size.
        """
        key = Fernet.generate_key()
        f = Fernet(key)
        token = f.encrypt(b"x" * reading_size)
        return len(token)
                    
    def get_encrypted_file_path(self, original_path):
        """Find the output windtalker file path. Usually just add a surfix
        "_WINDTALKER" to file name.
        """
        abspath = os.path.abspath(original_path)
        fname, ext = os.path.splitext(abspath)
        fname = fname + "_WINDTALKER"
        return fname + ext
    
    def get_encrypted_dir_path(self, original_path):
        """Find the output windtalker dir path. Usually just add a surfix
        "_WINDTALKER" to dir name.
        """
        abspath = os.path.abspath(original_path)
        return abspath + "_WINDTALKER"    
    
    def recover_path(self, encrypted_path):
        """Find the original path of encrypted file or dir.
        """
        return encrypted_path.replace("_WINDTALKER", "")
    
    def encrypt_file(self, path, output_path=None):
        """Encrypt a file. If output_path are not given, then try to use 
        file name with "_WINDTALKER" surfix.
        
        Overwrite an existing file is now allowed!
        """
        if not self._secret_key:
            raise SecretKeyNotGivenError(
                "You have to set a secret key to proceed.")
        
        if not output_path:
            output_path = self.get_encrypted_file_path(path)
        
        if os.path.exists(output_path):
            raise OverWriteFileError(
                "output path is already exists. => '%s'." % output_path)
        
        messenger.show("Encrypting %s ..." % path)
        
        with open(path, "rb") as f_input:
            with io.FileIO(output_path, "a") as f_output:
                while 1:
                    content = f_input.read(self._encrypt_chunk_size)
                    if content:
                        f_output.write(self.cipher.encrypt(content))
                    else:
                        break

        messenger.show("    Finished!")
                    
    def decrypt_file(self, path, output_path=None):
        """Decrypt a file. If output_path are not given, then try to remove 
        "_WINDTALKER" surfix in file name.
        
        Overwrite an existing file is now allowed!
        """
        if not self._secret_key:
            raise SecretKeyNotGivenError(
                "You have to set a secret key to proceed.")

        if not output_path:
            output_path = self.recover_path(path)

        if os.path.exists(output_path):
            raise OverWriteFileError(
                "output path is already exists. => '%s'." % output_path)
        
        messenger.show("Decrypting %s ..." % path)
        
        with open(path, "rb") as f_input:
            with io.FileIO(output_path, "a") as f_output:
                while 1:
                    try:
                        content = f_input.read(self._decrypt_chunk_size)
                    except:
                        raise PasswordError("Opps! Wrong magic word.")
                    if content:
                        f_output.write(self.cipher.decrypt(content))
                    else:
                        break
        
        messenger.show("    Finished!")
    
    def encrypt_dir(self, path, output_path=None):
        """Encrypt everything in a directory.
        """
        if not self._secret_key:
            raise SecretKeyNotGivenError(
                "You have to set a secret key to proceed.")
        
        if not output_path:
            output_path = self.get_encrypted_dir_path(path)
        
        if os.path.exists(output_path):
            raise OverWriteFileError(
                "output path is already exists. => '%s'." % output_path)
        
        for current_dir, _, file_list in os.walk(path):
            new_dir = current_dir.replace(path, output_path)
            os.mkdir(new_dir)
            for basename in file_list:
                old_path = os.path.join(current_dir, basename)
                new_path = os.path.join(new_dir, basename)
                self.encrypt_file(old_path, new_path)
    
    def decrypt_dir(self, path, output_path=None):
        """Decrypt everything in a directory.
        """
        if not self._secret_key:
            raise SecretKeyNotGivenError(
                "You have to set a secret key to proceed.")

        if not output_path:
            output_path = self.recover_path(path)

        if os.path.exists(output_path):
            raise OverWriteFileError(
                "output path is already exists. => '%s'." % output_path)

        for current_dir, _, file_list in os.walk(path):
            new_dir = current_dir.replace(path, output_path)
            os.mkdir(new_dir)
            for basename in file_list:
                old_path = os.path.join(current_dir, basename)
                new_path = os.path.join(new_dir, basename)
                self.decrypt_file(old_path, new_path)