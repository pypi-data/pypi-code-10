import re

REGEX_LINK = re.compile(r'(?P<link>http[s]?://\S+)'), '\033[34m\g<link>\033[39m'
REGEX_BOLD = re.compile(r'\*(?P<text>.+?)\*'), '\033[1m\g<text>\033[22m'
REGEX_UNDERLINE = re.compile(r'_(?P<text>.+?)_'), '\033[4m\g<text>\033[24m'
REGEX = [REGEX_LINK, REGEX_BOLD, REGEX_UNDERLINE]

ESCAPED_UNDERSCORE = '\\_', '_'
ESCAPED = [ESCAPED_UNDERSCORE]


def f(msg, *args, **kwargs):
    """

    >>> f("abc")
    'abc'

    >>> f("_abc_") == '\033[4mabc\033[24m'
    True

    >>> f("Before _first_ After _second_") == 'Before \x1b[4mfirst\x1b[24m After \x1b[4msecond\x1b[24m'
    True

    >>> f("*abc*") == '\033[1mabc\033[22m'
    True

    >>> f("Before *first* After *second*") == 'Before \x1b[1mfirst\x1b[22m After \x1b[1msecond\x1b[22m'
    True

    >>> f("https://www.zalando.de")  == '\033[34mhttps://www.zalando.de\033[39m'
    True
    """
    msg = msg.format(*args, **kwargs)
    for regex, replacement in REGEX:
        msg = regex.sub(replacement, msg)

    return msg
