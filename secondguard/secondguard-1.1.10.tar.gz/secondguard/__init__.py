# Not DRY, but best compromise for removing the learning curve for the library
"""
With this you can write code like the following:
>>> import secondguard
>>> secondguard.foo()
# or
>>> from secondguard import foo
>>> foo()
"""

from .api import ping
from .api import get_encryption_info
from .api import get_decryption_info

from .utils import is_valid_seed_hex
from .utils import is_seed_hash_pair
from .utils import derive_child_key

from .crypto import encrypt
from .crypto import decrypt

from .xlimit import sg_encrypt_secret
from .xlimit import sg_batch_encrypt_secrets
from .xlimit import sg_decrypt_secret
from .xlimit import sg_decrypt_from_priv_seed
