"""Misc utility functions
"""

import io
import re

import click


def print_command(args):
    """Nicely prints a command to console

    Args:
        args: command, as a list / tuple
    """
    # DEPRECATED
    click.echo(format_command(args, color=True))


def format_command(args, color=True):
    """Nicely format a command for printing.

    Will apply escaping when needed

    Args:
        args: command, as a list / tuple
    """

    escaped = (escape_argument(x) for x in args)

    if color:
        return ' '.join(highlight_command(x) for x in escaped)

    return ' '.join(escaped)


def format_envvar(name, value, color=True):
    if not color:
        return '{}={}'.format(name, repr(value))

    return '\x1b[1;32m{}=\x1b[0m{}'.format(
        name, highlight_envvar(repr(value)))


def escape_argument(text):
    """Escape a command argument
    """

    re_no_need_escaping = re.compile(r'^[0-9a-zA-Z_\.-]+$')
    if re_no_need_escaping.match(text):
        return text

    replacements = {
        '\\': '\\\\',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '"': '\\"',
    }

    def _escape_char(char):
        if char in replacements:
            return replacements[char]
        return char

    return '"{}"'.format(''.join(_escape_char(x) for x in text))


class SimpleTokenizer:
    def __init__(self, tokens):
        self._pattern = self._compile_lexer_re(tokens)

    def tokenize(self, text):
        for mo in self._pattern.finditer(text):
            typ = mo.lastgroup
            val = mo.group(typ)
            yield (typ, val)

    def _compile_lexer_re(self, tokens):
        return re.compile(
            '|'.join('(?P<{}>{})'.format(name, pattern)
                     for name, pattern in tokens))


HL_TOKENIZER = SimpleTokenizer([
    ('ESC_LBRACE', '{{'),
    ('ESC_RBRACE', '}}'),
    ('LBRACE', '{'),
    ('RBRACE', '}'),
    ('OTHER', '.'),
])


def highlight_replacements(text, C_NORMAL='\x1b[0;34m', C_BRACE='\x1b[0;36m'):

    output = io.StringIO()
    brace_depth = 0
    output.write(C_NORMAL)
    for ttyp, tval in HL_TOKENIZER.tokenize(text):
        if ttyp == 'LBRACE':
            brace_depth += 1
            if brace_depth == 1:
                output.write(C_BRACE)
            output.write(tval)

        elif ttyp == 'RBRACE':
            brace_depth -= 1
            output.write(tval)
            if brace_depth == 0:
                output.write(C_NORMAL)

        else:
            output.write(tval)
    output.write('\x1b[0m')
    return output.getvalue()


def highlight_command(text):
    return highlight_replacements(
        text, C_NORMAL='\x1b[0;34m', C_BRACE='\x1b[0;36m')


def highlight_envvar(text):
    return highlight_replacements(
        text, C_NORMAL='\x1b[0;32m', C_BRACE='\x1b[0;33m')
