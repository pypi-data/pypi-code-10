# -*- coding: utf-8 -*-
"""Parse a django template and find all template variables that are used.
   Output the template variables in a format that can be included in the
   template to verify the values of all context variables.
"""

import sys
import re
from cStringIO import StringIO


def name(t):
    """The name of the tag.
    """
    txt = t.strip(' {%').split()[0]
    return txt


def content(t):
    """The content of the tag.
    """
    if is_tag(t):
        try:
            return ' '.join(t.strip(' {%}').split()[1:])
        except IndexError:
            return ""
    else:
        return t.strip(' {}')


def is_tag(t):
    """Is `t` a tag?
    """
    return t.strip().startswith('{%')


def is_endtag(t):
    """Is `t` an end-tag?
    """
    if not is_tag(t):
        return False
    return name(t).startswith('end')


class Node(object):
    pass


class Value(Node):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "{{ %s }} ===> %r" % (self.val, list(self.fvars()))

    def fvars(self):
        return {self.val.split('|')[0]}


class Tag(Node):
    def __init__(self, name, content=None):
        self.name = name
        self.content = content

    def is_identifier(self, txt):
        return re.match('^[\w\.]+$', txt)

    def find_identifiers(self, txt):
        return set(t for t in txt.split() if self.is_identifier(t))

    def __repr__(self):
        return "{%% %s %s %%} ==> %r" % (self.name, self.content, list(self.fvars()))

    def matches(self, endtag):
        return name(endtag)[3:] == self.name

    def fvars(self):
        return self.find_identifiers(self.content) if self.content else set()

    def dvars(self):
        return set()


class NoOpTag(Tag):
    def __repr__(self):
        return ""

    def fvars(self):
        return set()


# class IncludeTag(Tag):
#     def __repr__(self):
#         return ""
#
#     def fvars(self):
#         return set()


class IfTag(Tag):
    def fvars(self):
        return self.find_identifiers(self.content) - {'and', 'or', 'not'}


class ForTag(Tag):
    def fvars(self):
        return self.find_identifiers(self.content.split(' in ', 1)[1])

    def dvars(self):
        return self.find_identifiers(self.content.split(' in ', 1)[0])


class WithTag(Tag):
    def fvars(self):
        if ' as ' in self.content:
            return self.find_identifiers(self.content.rsplit(' as ', 1)[0])
        else:
            return self.find_identifiers(self.content.split('=', 1)[1])

    def dvars(self):
        if ' as ' in self.content:
            return self.find_identifiers(self.content.rsplit(' as ', 1)[1])
        else:
            return self.find_identifiers(self.content.split('=', 1)[0])


def make_tag(name, content=None):
    return {
        'if': IfTag,
        'elif': IfTag,
        'for': ForTag,
        'with': WithTag,
        'load': NoOpTag,
        'include': NoOpTag,
    }.get(name, Tag)(name, content)


class Block(Node):
    def __init__(self, name, tag, block):
        self.name = name
        self.tag = tag
        self.block = block
        self.indent_level = 0

    def indent(self, txt, n):
        return '\n'.join(['    ' * n + line for line in txt.splitlines()])

    def fvars(self):
        res = self.tag.fvars()
        for item in self.block:
            res |= {fv.split('.', 1)[0] for fv in item.fvars()}
        return res - self.dvars() - {'request'}

    def dvars(self):
        return self.tag.dvars()

    def display_fvars(self):
        return "{\n    " + ',\n    '.join(["%s: {{%s}}" % (fv, fv) for fv in self.fvars()]) + '\n}'

    def __repr__(self):
        # print self.fvars()
        block = '\n'.join(repr(s) for s in self.block)
        return "\n%s%s\n%s\n%s\n%s" % (
            self.indent("", self.indent_level),
            self.display_fvars(),
            self.indent(repr(self.tag), self.indent_level),
            self.indent(block, self.indent_level + 1),
            '{%% end%s %%}' % self.name
        )
        # return "\n%sFV: %s\tDV: %s\n%s\n%s\n%s" % (
        #     self.indent("", self.indent_level),
        #     self.display_fvars(),
        #     list(self.tag.dvars()),
        #     self.indent(repr(self.tag), self.indent_level),
        #     self.indent(block, self.indent_level + 1),
        #     '{%% end%s %%}' % self.name
        # )


def nest(words):
    """Nest start/end tags into blocks recursively.
    """
    stack = [Tag('-program')]

    def prstack():
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
            stack.append(make_tag(name(word), content(word)))
        else:
            # print "SHIFT VAL", word
            stack.append(Value(content(word)))

    return stack[0]


# class Render(object):
#     def __init__(self, content):
#         self.content = content
#         self.out = StringIO()
#         self.curlevel = 0
#
#     def value(self):
#         return self.out.getvalue()
#
#     def render(self, item=None):
#         if item is None:
#             item = self.content[0]
#
#         tag = item[0]
#
#         if tag.startswith('block:'):
#             tag = 'block'
#
#         #print '[I]', item, 'CALLING:', getattr(self, 'render_' + tag).__name__ , item
#         try:
#             getattr(self, 'render_' + tag)(item)
#         except:
#             print '='*80
#             print self.out.getvalue()
#             raise
#
#     def render_block(self, block):
#         print >>self.out, "{%% %s %%}" % block[0]
#         if len(block) > 1:
#             for item in block[1]:
#                 self.render(item)
#         print >>self.out, "{%% end%s %%}" % block[0]
#
#     def render_tag(self, tag):
#         print >>self.out, "{%% %s %%}" % (' '.join(tag[1:]))
#
#     def render_val(self, item):
#         print >>self.out, "{{ %s }}" % item[1]
            

def tokenize(t):
    tag_and_vals = []
    txt = re.sub(r'{#.*?#}', '', t)
    tag_and_vals += re.findall(r'{(?:%|{).*?(?:}|%)}', txt)
    return tag_and_vals

#
# def render(txt):
#     r = Render(nest(tokenize(txt)))
#     r.render()
#     return r.value()


def templatevars(t):
    """Will return the template variables...
    """
    tag_and_vals = []
    txt = re.sub(r'{#.*?#}', '', t)
    tag_and_vals += re.findall(r'{(?:%|{).*?(?:}|%)}', txt)
    return nest(tag_and_vals)


def main():
    """cli entry point.
    """
    import pprint
    template = open(sys.argv[1]).read()
    template = re.sub(r'TEMPLATEVARS:.*?:TEMPLATEVARS', "", template)
    txt = repr(nest(tokenize(template)))
    txt = txt.replace('{% end-program %}', '</pre>:TEMPLATEVARS' + '<br>' * 5)
    txt = txt.replace('{% -program None %} ==> []', '')
    # txt = re.sub(r'{%\s*load.*?%}', '', txt)
    txt = 'TEMPLATEVARS:<pre>' + txt
    print txt
    # pprint.pprint()
    # print render(template)


if __name__ == "__main__":
    main()
