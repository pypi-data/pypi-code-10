from __future__ import absolute_import, unicode_literals

import string

from django.utils.crypto import get_random_string

from ..config import config

_DEFAULT_RAND_LENGTH = config.DEFAULT_PASSWORD_LENGTH


def random_string(length=_DEFAULT_RAND_LENGTH, num=True, special=True, letters=None):
    alphabet = string.ascii_letters
    if(num):
        alphabet += string.digits
    if(special):
        alphabet += '!"$%^&*()_+=-[]{}#@~,./<>?'
    return get_random_string(length, letters or alphabet)


def random_ascii_letters(length=_DEFAULT_RAND_LENGTH):
    return random_string(length, letters=string.ascii_letters)


def random_digits(length=_DEFAULT_RAND_LENGTH):
    return random_string(length, letters=string.digits)
