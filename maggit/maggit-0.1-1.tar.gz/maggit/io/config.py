# This file is part of maggit.
#
# Copyright 2015 Matthieu Gautier <dev@mgautier.fr>
#
# Pit is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# Additional permission under the GNU Affero GPL version 3 section 7:
#
# If you modify this Program, or any covered work, by linking or
# combining it with other code, such other code is not for that reason
# alone subject to any of the requirements of the GNU Affero GPL
# version 3.
#
# You should have received a copy of the GNU Affero General Public License
# along with maggit.  If not, see http://www.gnu.org/licenses
#
# In summary:
# - You can use this program for no cost.
# - You can use this program for both personal and commercial reasons.
# - You do not have to share your own program's code which uses this program.
# - You have to share modifications (e.g bug-fixes, improvements) you've made to this program.

import sys

class EOF(Exception):
    pass

class Stream:
    def __init__(self, stream):
        self.stream = stream
        self._unpick = None
        self._last = None

    def pop(self):
        if self._last:
            c, self._last = self._last, None
        else:
            c = self.stream.read(1)
        self._unpick = c
        if c == b'':
            raise EOF()
        return c

    def get(self):
        if self._last is None:
            self._last = self.stream.read(1)
        self._unpick = None
        if self._last == b'':
            raise EOF()
        return self._last

    def unpick(self):
        assert self._unpick is not None
        assert not self._last
        self._last, self._unpick = self._unpick, None

    def eof(self):
        try:
            self.get()
            return False
        except EOF:
            return True

class SectionContent:
    def __init__(self, name, subname):
        self.before, self.leading, self.innerStart, self.name, self.innerEnd, self.ending = b'\n', b'', b'', name, b'', b''
        if subname:
            self.innerSep, self.subname = b' ', subname

    def __repr__(self):
        return repr(self.__dict__)

class Section:
    def __init__(self, name, subname):
        self.name = name
        self.subname = subname
        self.variables = []
        self.content = SectionContent(name, subname)

    def add_variable(self, var):
        self.variables.append(var)
        var.section = self

    def set_content(self, content):
        self.content.leading, self.content.innerStart, self.content.name, *content, self.content.innerEnd, self.content.ending = content
        if content:
            self.content.innerSep, self.content.subname = content

    def update_leading_space(self, space_comment):
        self.content.before = space_comment

    def __eq__(self, other):
        return (self.name, self.subname) == other[0] and self.variables == other[1]

    def __repr__(self):
        return "<Section %(name)s:%(subname)s %(content)s>"%self.__dict__

    def pretty_content(self):
        out = self.content.before + self.content.leading + b'[' + self.content.innerStart + self.content.name
        try:
            out += self.content.innerSep + b'"' + self.content.subname + b'"'
        except AttributeError:
            pass
        out += self.content.innerEnd + b']' + self.content.ending
        return out

    def get_full_sectionName(self):
        if self.subname:
            return b'.'.join((self.name, self.subname))
        return self.name


class VariableContent:
    def __init__(self, name, value):
        self.before, self.leading, self.name, self.ending = b'\n', b'\t', name, b''
        if value:
            self.preSep, self.postSep, self.value = b' ', b' ', value

    def __repr__(self):
        return repr(self.__dict__)

class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.content = VariableContent(name, value)

    def set_content(self, content):
        self.content.leading, self.content.name, *content, self.content.ending = content
        if content:
            self.content.preSep, self.content.postSep, self.content.value = content

    def set_value(self, value):
        self.value = self.content.value = value
        self.content.leading = b'\t'

    def update_leading_space(self, space_comment):
        self.content.before = space_comment

    def __eq__(self, other):
        return (self.name, self.value) == other

    def __repr__(self):
        return "<Variable %(name)s:%(value)s %(content)s>"%self.__dict__

    def pretty_content(self):
        out = self.content.before + self.content.leading + self.content.name
        try:
            out += self.content.preSep + b'=' + self.content.postSep + self.content.value
        except AttributeError:
            pass
        out += self.content.ending
        return out


def regen_section(content):
    assert content[0] == 'section'
    out = b'[' + content[1] + content[2] + content[3]
    content = content[4:]
    if content:
        out += b'"' + content[0] + b'"' + content[1]
    out += b']'
    return out

def regen_variable(content):
    assert content[0] == 'variable'
    out = content[1] + content[2]
    content = content[3:]
    if content:
        out += b'=' + content[0] + content[1] + content[2]
    return out


def pretty_value(value):
    if value is None:
        return b''
    if value is True:
        return b' = true'
    if value is False:
        return b' = false'
    if isinstance(value, bytes):
        return b' = '+value
    return (" = %s"%value).encode()

escape_quote_code = { b'"'[0] :b'"'[0],
                      b'\\'[0]:b'\\'[0],
                      b'n'[0] :b'\n'[0],
                      b't'[0] :b'\t'[0],
                      b'b'[0] :b'\b'[0]
              }
def strip_quote(value):
    out = bytearray()
    stream = iter(value)
    for v in stream:
        if v == b'"'[0]:
            continue
        if v == b'\\'[0]:
            v = escape_quote_code[next(stream)]
        out.append(v)
    return bytes(out)

def eval_value(value):
    value = strip_quote(value)
    try:
        v = int(value)
        return v
    except ValueError:
        pass

    lower = value.lower()
    if lower in (b'true', b'yes', b'on', b'1'):
        return True
    if lower in (b'false', b'no', b'off', b'0'):
        return False
    return value

ending = {True:b'\n', False:b';#\n'}
escape_code = { b'"':b'\\"',
                b'\\':b'\\',
                b'\n':b'\n',
                b'n':b'\\n',
                b't':b'\\t',
                b'b':b'\\b'
              }
def read_value(stream):
    token = b''
    enclosed = False
    space = 0
    while True:
        try:
            c = stream.pop()
        except EOF:
            break
        if c in ending[enclosed]:
            stream.unpick()
            break
        if c == b' ':
            space += 1
            continue
        token += b' '*space
        space = 0
        if c == b'"':
            enclosed = not enclosed
            #continue
        if c == b'\\':
            c = escape_code[stream.pop()]
        token += c
    ending_space = b' '*space
    return bytes(token), ending_space

def read_token(stream, valid, escape=False):
    token = b''
    while True:
        try:
            c = stream.pop()
        except EOF:
            break
        if not valid(c):
            stream.unpick()
            break
        if escape and c == b'\\':
            c = stream.pop()
        token += c
    return bytes(token)

def space(stream):
    return read_token(stream, lambda c: c in b' \t')

def space_comment(stream, accept_newline=False):
    token = b''
    comment = False
    while True:
        try:
            c = stream.pop()
        except EOF:
            break
        if c in b';#':
            comment = True
        if c == b'\n':
            if accept_newline:
                token += c
            else:
                stream.unpick()
            break
        if not comment and c not in b' \t':
            stream.unpick()
            break
        token += c
    return bytes(token)

def read_line(stream):
    ret = None
    content = []
    v_space = b''

    content.append(space(stream))
    nextc = stream.pop()

    if nextc == b'[':
        # this is a section
        content.append(space(stream))
        sectionName = read_token(stream, lambda c: c.isalnum() or c in b'-.')
        ret = Section(sectionName, None)
        content.append(sectionName)
        content.append(space(stream))
        nextc = stream.pop()
        if nextc == b'"':
            subSectionName = read_token(stream, lambda c: c != b'"', escape=True)
            ret.subname = subSectionName
            content.append(subSectionName)
            assert stream.pop() == b'"'
            content.append(space(stream))
            nextc = stream.pop()
        assert nextc == b']'
    elif nextc not in b';#\n':
        # variable def
        stream.unpick()
        variableName = read_token(stream, lambda c: c.isalnum() or c in b'-')
        content.append(variableName)
        variableName = variableName.lower()
        ret = Variable(variableName, None)
        v_space = space(stream)
        try:
            nextc = stream.pop()
        except EOF:
            nextc = None
        if nextc == b'=':
            content.append(v_space)
            content.append(space(stream))
            variableValue, v_space = read_value(stream)
            content.append(variableValue)
            variableValue = eval_value(variableValue)
            ret.value = variableValue
        else:
            stream.unpick()
    else:
        stream.unpick()

    content.append(v_space+space_comment(stream, ret is None))

    return ret, content

def read_UTF8BOM(stream):
    BOM = b"\xef\xbb\xbf"
    while BOM:
        try:
            nextc = stream.pop()
        except EOF:
            nextc = b''
        print(BOM, nextc)
        if nextc == BOM[:1]:
            BOM = BOM[1:]
        else:
            if len(BOM) != 3:
                #partial BOM
                raise InvalidConfigFormat("Do not accept file with partial BOM\n")
            stream.unpick()
            break
    return not bool(BOM)

def read_file(stream):
    stream = Stream(stream)
    current_space_comment = b''
    sections = []
    withBOM = read_UTF8BOM(stream)
    while not stream.eof():
        what, content = read_line(stream)
        if what is None:
            current_space_comment += content[0]+content[1]
            print(what, content)
            continue
        what.set_content(content)
        what.update_leading_space(current_space_comment)
        current_space_comment = b''
        print(what, content)
        if isinstance(what, Section):
            sections.append(what)
        if isinstance(what, Variable):
            sections[-1].add_variable(what)
    return sections, current_space_comment, withBOM


def pretty_sections(sections):
    current_section = None
    for section in sections:
        yield section.pretty_content()
        for var in section.variables:
            yield var.pretty_content()

def gen_file(sections, ending, withBOM):
    bom = b"\xef\xbb\xbf" if withBOM else b''
    return bom + b''.join(pretty_sections(sections)) + ending

class Config:
    def __init__(self, filename):
        self.filename = filename

    def read_file(self):
        with open(self.filename, "rb") as f:
            variables = read_file(f)
        return variables

