# -*- coding: utf-8 -*-
import re

from dktemplate.ast import IfTag, ForTag, WithTag, NoOpTag, Tag, Block, Value, IncludeTag
from dktemplate.tokenize import name, content, tokenize, is_tag, is_endtag


def parse_file(fname):
    return parse(open(fname).read(), fname)


def parse(txt, fname=None):
    """Parse template text.
    """
    txt = re.sub(r'{#\s*dk-template:\s*noparse\s*#}.*?{#\s*dk-template:\s*end-noparse\s*#}', "", txt)
    return nest(tokenize(txt), fname)


def make_tag(name, content=None, fname=None):
    return {
        'if': IfTag,
        'elif': IfTag,
        'for': ForTag,
        'with': WithTag,
        'load': NoOpTag,
        'include': IncludeTag,
    }.get(name, Tag)(name, content, fname)


def nest(words, fname):
    """Nest start/end tags into blocks recursively.
    """
    stack = [Tag('-program')]

    def prstack():  # pragma:nocover
        """Print stack contents.
        """
        print "STACK:...."
        for item in stack:
            print item

    for word in words + ['{% end-program %}']:
        # print "\WORD:", word
        # prstack()

        if is_endtag(word):
            tagname = name(word)[3:]
            # print "REDUCE", tagname
            block = []
            while 1:
                item = stack.pop()
                found = isinstance(item, Tag) and item.matches(word)
                # print '    POPPED', item, 'FOUND' if found else ""
                if found:
                    stack.append(Block(item.name, item, block[::-1]))
                    break
                else:
                    block.append(item)
        elif is_tag(word):
            # print "SHIFT TAG", name(word)
            stack.append(make_tag(name(word), content(word), fname))
        else:
            # print "SHIFT VAL", word
            stack.append(Value(content(word)))

    return stack[0]
