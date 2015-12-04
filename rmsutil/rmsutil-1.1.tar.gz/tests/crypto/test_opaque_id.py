from __future__ import unicode_literals

import re

import pytest

from rmsutil import crypto

_KEY_512 = ('b_n-TfsJZFoPsUH_O-E1SNBPHWkk8QCX65my4gPoYmPAf8tGsyTCyrmHKuFARZf5p'
            '1cMI8PGIINXuucz7sDltQ==')
_KEY_136 = 'dxSbxWTs-y0XSh2bRdLCLJk='
_KEY_128 = 'ZR9L42pvF1Qlx5tZtZEs0Q=='
_KEY_120 = 'orAr0SwFycVgP-g6iKDW'

_IDENTIFIER = '123894'


@pytest.mark.parametrize(
    'key, message',
    [
        (_KEY_128, _IDENTIFIER),
        (_KEY_136, _IDENTIFIER),
        (_KEY_512, _IDENTIFIER),
    ]
)
def test_opaque_id(key, message):
    oid = crypto.opaque_id(key, message)
    assert re.match('[-_a-zA-Z0-9]{43}=$', oid)


@pytest.mark.parametrize(
    'key',
    [
        '',  # Empty
        _KEY_120,  # Too short by 1 byte
        _KEY_128[:-1],  # Incorrect padding
    ]
)
def test_opaque_id_errors(key):
    with pytest.raises((ValueError, TypeError)):
        crypto.opaque_id(key, _IDENTIFIER)
