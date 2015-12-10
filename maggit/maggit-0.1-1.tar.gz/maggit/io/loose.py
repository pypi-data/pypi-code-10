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

from binascii import unhexlify, hexlify
import hashlib
import zlib
import time
import os
from maggit.const import ObjectType

def bytes_join(function):
    def wrapper(*args, **kwords):
        return b''.join(function(*args, **kwords))
    return wrapper

def expand_zlib(compressed):
    content = zlib.decompress(compressed)
    index = 0
    type_ = []
    size = []
    found = False
    for index, byte in enumerate(content, 1):
        if byte == 0:
            break
        if byte == b' '[0]:
            found = True
            continue
        if found:
            size.append(byte)
        else:
            type_.append(byte)
    type_ = bytes(type_)
    type_ = ObjectType(type_)
    size = int(bytes(size))
    assert size == len(content)-index
    return type_, content[index:]

def object_rawsha(type_, content):
    """Generate the raw content and the sha of a object content.

    Arguments:
        type_ (bytes): The type of the object.
        content (bytes): The content of the object (without header).

    Returns:
        bytes, bytes:

        A tuple (raw, sha) where:

         - raw is the full content of the object (with header).
         - sha is the sha of the object.
    """
    type_ = bytes(type_)
    sha = hashlib.sha1()
    def iter_content():
        sha.update(type_)
        yield type_
        sha.update(b' ')
        yield b' '
        c = '%d'%len(content)
        c = c.encode()
        sha.update(c)
        yield c
        c = bytes([0])
        sha.update(c)
        yield c
        sha.update(content)
        yield content
    raw = b''.join(iter_content())
    return raw, sha.digest()

def object_sha(type_, content):
    """Generate the sha of a object content.

    Is the bit more performant than object_rawsha(...)[1] as the raw content is
    not generated.

    Arguments:
        type_ (bytes): The type of the object.
        content (bytes): The content of the object (without header).

    Returns:
        The sha of the object.
    """
    type_ = bytes(type_)
    sha = hashlib.sha1()
    sha.update(type_)
    sha.update(b' ')
    c = '%d'%len(content)
    sha.update(c.encode())
    sha.update(bytes([0]))
    sha.update(content)
    return sha.digest()

def object_sha_from_raw(raw):
    """Generate the sha of a object from its content.

    Arguments:
        raw(bytes): The content of the object (with header)

    Returns:
        The sha of the object.
    """
    return hashlib.sha1(raw).digest()

def object_content(filepath):
    """Return the content of a loose object.

    Arguments:
        filepath: The path of the loose object.

    Returns:
        bytes, bytes:

        A tuple (type, content) where:

         - type is the type of the object.
         - content is the content of the object (without header).
    """
    with filepath.open(mode="br") as f:
        return expand_zlib(f.read())

def object_write(filepath, content, compress_level=1):
    """Correctly create the loose object file.

    Arguments:
        filepath : The path of the loose object to write.
        content(bytes) : The full content (with header) to write.
        compress_level(int) : The compression level to use (default=1).
    """
    try:
        filepath.parent.mkdir(parents=True)
    except FileExistsError:
        pass
    tmpfile = filepath.with_name('tmp_obj_XXXXXX')
    with tmpfile.open(mode="bw") as f:
        f.write(zlib.compress(content, compress_level))
    try:
        os.link(str(tmpfile), str(filepath))
    except FileExistsError:
        # Do not fail if path already exists,
        # this is normal behavior in git
        pass
    tmpfile.unlink()

def tree_parse(content):
    """Parse a tree content.

    Arguments:
        content(bytes): The content to parse (without header).

    Returns:
        List[Tuple[bytes, Tuple[bytes, bytes]]]:

        A list of (path, (mode, sha)) where :

         - path is the name of the entry.
         - mode is the git mode.
         - sha is the sha of the blob/tree object.
    """
    return list(_tree_parse(content))

def _tree_parse(content):
    index = 0
    max_ = len(content)
    while index < max_:
        start = index
        index = content.find(b' ', start)
        mode_  = content[start:index]

        start = index+1
        index = content.find(0, start)
        name_ = content[start:index]

        index += 1
        sha_ = content[index:index+20]

        yield name_, (mode_, sha_)
        index += 20

_to_bytes = lambda path, mode_sha : mode_sha[0] + b' ' + path + bytes([0]) + mode_sha[1]
@bytes_join
def tree_gen(entries):
    """Generate a bytes corresponding to a tree.

    Git sort entries in a tree by path. This is still a valid tree object
    if entries are not sorted but if you want to be fully compliant with git, you
    must sort the entries before using tree_gen.
    Maggit itself do not care of the entries' order. However the sha of the object
    will differ if the order differ. This can be pretty confusing so you should
    sort the entries (or at least ensure a 'constant ordering').

    Arguments:
        entries(List[Tuple]): A list of entries in the tree.
                              Tuples must be (path, (mode, sha)) where
                               - path is the name of the entry (bytes)
                               - mode is a valid git mode bytes
                               - sha is the sha of the blob/tree object (bytes)

                              The entries MUST be sort by path to be valid.

    Returns:
        A bytes corresponding to the tree.
        The bytes doesn't include the object header.
    """
    return (_to_bytes(*c) for c in entries)

def commit_parse(content):
    """Parse a commit content.

    Arguments:
        content(bytes): The content to parse (without header).

    Returns:
        bytes, list[bytes], bytes, bytes, bytes:

        A tuple (tree, parents, message, author, committer) where:

         - tree is the sha of the tree object of the commit(unhexlified bytes).
         - parents is a list of sha of the parents commit.
         - message is the message of the commit.
         - author is the name (b'name <email> timestamp') of the author.
         - author is the name (b'name <email> timestamp') of the committer.
    """
    parents = []
    message, message_start = [], False
    # sha can contains '\n' and so, the split is not good.
    # If've got a sha length < 20, this is probably cause of a '\n'
    # Next line will containt the rest of the sha
    # Keep the entry and complete when next line
    current_type, current_content = None, None
    for line in content.split(b'\n'):
        if message_start:
            message.append(line)
            continue

        if current_type:
            type_, other = current_type, (current_content+line,)
            current_type = None
        else:
            type_, *other = line.split(b' ')

        if type_ in (b'tree', b'parent'):
            if len(other[0]) < 20:
                current_type = type_
                current_content = other[0] + b'\n'
                continue

        if type_ == b'tree':
            tree = unhexlify(other[0])
            continue
        if type_ == b'parent':
            parents.append(unhexlify(other[0]))
            continue
        if type_ == b'author':
            author = b' '.join(other)
            continue
        if type_ == b'committer':
            committer = b' '.join(other)
            continue
        if type_ == b'mergetag':
            continue
        if type_ == b'':
            message_start = True
            continue
        # We should not go there !!
        assert False
    return tree, parents, message, author, committer

@bytes_join
def commit_gen(treesha, message, author, authorDate, committer, committerDate, parents=[]):
    """Generate a bytes corresponding to a commit.

    Arguments:
        treesha(unhexlified bytes): The sha of the tree.
        message(bytes): The message of the commit.
        author(bytes): A git valid author b'name <email>'.
        authorDate(bytes): A git valid timestamp to associate to the author.
        committer(bytes): A git valid commiter b'name <email>'.
        committerDate(bytes):   A git valid timestamp to associate to the committer.
        parents(list[unhexlified bytes]): The shas of the parents of the commit.

    Returns:
        A bytes corresponding to the commit.
        The bytes doesn't include the object header.
    """
    if not authorDate or not committerDate:
        now = time.time()
        authorDate = authorDate or (bytes(str(now), 'ascii') + b' +0000')
        committerDate = committerDate or (bytes(str(now), 'ascii') + b' +0000')
    yield b'tree ' + hexlify(treesha) + b'\n'
    for parent in parents:
        yield b'parent ' + hexlify(parent) + b'\n'
    yield b'author ' + author + b' ' + authorDate + b'\n'
    yield b'committer ' + committer + b' ' + committerDate + b'\n\n'
    yield message

def tag_parse(content):
    """Parse a tag content.

    Arguments:
        content(bytes): The content to parse (without header).

    Returns:
        bytes, bytes, bytes, bytes, bytes:

        A tuple (object, objecttype, tag, tagger, message) where:

         - object is the sha of the tagged object (unhexlified bytes).
         - objecttype is the type of the tagged object.
         - tag is the name of the tag.
         - tagger is the name (b'name <email> timestamp') of the tagger.
         - message is the message of the tag.
    """
    message, message_start = [], False
    # sha can contains '\n' and so, the split is not good.
    # If've got a sha length < 20, this is probably cause of a '\n'
    # Next line will containt the rest of the sha
    # Keep the entry and complete when next line
    current_type, current_content = None, None
    for line in content.split(b'\n'):
        if message_start:
            message.append(line)
            continue

        if current_type:
            type_, other = current_type, (current_content+line,)
            current_type = None
        else:
            type_, *other = line.split(b' ')

        if type_ == b'object':
            if len(other[0]) < 20:
                current_type = type_
                current_content = other[0] + b'\n'
            else:
                object_ = unhexlify(other[0])
            continue
        if type_ == b'type':
            objtype_ = other[0]
            continue
        if type_ == b'tag':
            tag = b' '.join(other)
            continue
        if type_ == b'tagger':
            tagger = b' '.join(other)
            continue
        if type_ == b'':
            message_start = True
            continue
        # We should not go there !!
        assert False

    return object_, objtype_, tag, tagger, message

@bytes_join
def tag_gen(objectsha, objecttype, tag, tagger, tagDate, message):
    """Generate a bytes corresponding to a tag.

    If authorDate or committerDate are False, the date is 'now'.

    Arguments:
        objectsha(unhexlified bytes): The sha of the tagged object.
        objecttype(bytes): The type of the tagged object.
        tag(bytes): The name of the tag.
        tagger(bytes): A git valid tagger b'name <email>'.
        tagDate(bytes): A git valid timestamp to associate to the author.
        message(bytes): The message of the tag.

    Returns:
        A bytes corresponding to the tag.
        The bytes doesn't include the object header.
    """
    end = b'' if message[-1] == b'\n'[0] else b'\n'
    return (b'object ', hexlify(objectsha),  b'\n',
            b'type '  , bytes(objecttype),         b'\n',
            b'tag '   , tag,                       b'\n',
            b'tagger ', tagger, b' ', tagDate,     b'\n\n',
            message, end)
