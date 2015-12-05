# -*- coding: utf-8 -*-


def tokenize(text):
    """
    Convert a text to tokens.

    Example:
        >>> print(tokenize('Hello world!'))
        ['Hello', 'world', '!']

    :param    text: Text to tokenize.
    :type     text: str
    :return:        List of tokens.
    :rtype:         list
    """

    # Find delimiters and make sure that these are isolated tokens
    delimiters = ['.', ',', ':', ';', '?', '!', '<', '>', '[', ']', '(', ')', '"']
    for delimiter in delimiters:
        text = text.replace(delimiter, ' ' + delimiter + ' ')

    # Now find all the tokens
    tokens = []
    for token in text.split(' '):
        if len(token) > 0:
            tokens.append(token)

    # And give back the tokens
    return tokens
