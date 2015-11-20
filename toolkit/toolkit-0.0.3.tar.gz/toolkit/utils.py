# coding=utf8

import hashlib


def md5(s):
    """
    Returns :class:`str` object after md5 encrypt.

    :param s: :class:`str`, the str to md5 encrypt.
    """
    return hashlib.new('md5', s).hexdigest()


def sha1(s):
    """
    Returns :class:`str` object after sha1 encrypt.

    :param s: :class:`str`, the str to sha1 encrypt.
    """
    return hashlib.new('sha1', s).hexdigest()
