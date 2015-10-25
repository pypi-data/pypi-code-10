from random import choice

from .pyclr import finished_styles


def rainbow(s):
    colors = ['red', 'yellow', 'green', 'blue', 'magenta']
    result, i = '', 0
    for c in s:
        if c == ' ':
            result += ' '
        else:
            result += finished_styles[colors[i % 5]](c)
            i += 1
    return result


def zebra(s):
    result, i = '', 0
    for c in s:
        if i % 2 == 0:
            result += finished_styles['inverse'](c)
        else:
            result += c
        i += 1
    return result


def america(s):
    colors = ['red', 'white', 'blue']
    result, i = '', 0
    for c in s:
        if c == ' ':
            result += ' '
        else:
            result += finished_styles[colors[i % 3]](c)
            i += 1
    return result


def random(s):
    colors = ['underline', 'inverse', 'grey', 'yellow', 'red', 'green',
              'blue', 'white', 'cyan', 'magenta']
    result = ''
    for c in s:
        if c == ' ':
            result += ' '
        else:
            result += finished_styles[choice(colors)](c)
    return result
