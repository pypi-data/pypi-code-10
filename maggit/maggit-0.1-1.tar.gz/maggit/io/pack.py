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

from zlib import decompress
from binascii import unhexlify, hexlify, Error as binasciiError
from struct import unpack_from
import ctypes
from mmap import mmap, ACCESS_READ
from maggit.const import ObjectType

__all__ = ('GitPack', 'GitPackIndex')

_wrapping_struct_cache = {}
def read_ctypes(buff, ctypes_):
    try:
        wrapping_struct, size = _wrapping_struct_cache[ctypes_]
    except KeyError:
        wrapping_struct = type('Wrap_%s'%ctypes_, (ctypes.BigEndianStructure, ), {'_fields_':(('v', ctypes_),)})
        size = ctypes.sizeof(wrapping_struct)
        _wrapping_struct_cache[ctypes_] = wrapping_struct, size

    ret =  wrapping_struct.from_buffer_copy(buff[:size]).v
    return ret, buff[size:]

class SizeChar(ctypes.BigEndianStructure):
    _fields_ = [ ('cont', ctypes.c_uint8, 1),
                 ('size'    , ctypes.c_uint8, 7)
               ]

def read_delta_size(data):
    sizeChar, data = read_ctypes(data, SizeChar)
    size = sizeChar.size
    shift = 7
    while sizeChar.cont:
        sizeChar, data = read_ctypes(data, SizeChar)
        size =  size | (sizeChar.size << shift)
        shift += 7
    return size, data

def delta_chunk(base, data):
    while len(data):
        cmd, data = unpack_from("!B", data)[0], data[1:]
        if cmd & 0x80:
            cp_offset = 0
            if cmd & 0x01:
                cp_offset, data = unpack_from("!B", data)[0], data[1:]
            if cmd & 0x02:
                off, data = unpack_from("!B", data)[0], data[1:]
                cp_offset |= (off << 8)
            if cmd & 0x04:
                off, data = unpack_from("!B", data)[0], data[1:]
                cp_offset |= (off << 16)
            if cmd & 0x08:
                off, data = unpack_from("!B", data)[0], data[1:]
                cp_offset |= ((off&127) << 24)
            cp_size = 0
            if cmd & 0x10:
                cp_size, data = unpack_from("!B", data)[0], data[1:]
            if cmd & 0x20:
                size, data = unpack_from("!B", data)[0], data[1:]
                cp_size |= (size << 8)
            if cmd & 0x40:
                size, data = unpack_from("!B", data)[0], data[1:]
                cp_size |= (size << 16)
            if not cp_size:
                cp_size = 0x10000
            #if cp_offset+cp_size<cp_size or cp_offset+cp_size>len(base):
            #    break
            yield base[cp_offset:cp_offset+cp_size]
        elif cmd:
            out, data = data[:cmd], data[cmd:]
            yield out
        else:
            raise Exception


def apply_patch(base, delta_data):
    data = memoryview(delta_data)
    src_size, data = read_delta_size(data)
    dst_size, data = read_delta_size(data)
    content = b''.join(delta_chunk(base, data))
    assert dst_size == len(content)
    return content

class pack_first_obj_header(ctypes.BigEndianStructure):
    _fields_ = [ ('cont', ctypes.c_uint8, 1),
                 ('type'    , ctypes.c_uint8, 3),
                 ('size'    , ctypes.c_uint8, 4)
               ]

class pack_other_obj_header(ctypes.BigEndianStructure):
    _fields_ = [ ('cont', ctypes.c_uint8, 1),
                 ('size'    , ctypes.c_uint8, 7)
               ]

typeName = {1: b'commit',
            2: b'tree',
            3: b'blob',
            4: b'tag'
           }

class GitPack:
    """A git pack file.

    Arguments:
            packfile(path): The path of the packfile.
            idxfile(:class:`~maggit.io.pack.GitPackIndex`): The index associated to the pack.
    """
    def __init__(self, packfile, idxfile):
        self.packfile = packfile.open("rb")
        self.mmap = mmap(self.packfile.fileno(), 0, access=ACCESS_READ)
        self.mview = memoryview(self.mmap)
        self.idxfile = idxfile
        self.read_header()
        self.__cache = {}

    def close(self):
        self.mview.release()
        self.mmap.close()
        self.packfile.close()

    def __del__(self):
        self.close()
        self.packfile = None

    def read_header(self):
        self.type_, self.version_number, self.nb_objects = unpack_from("!4s i i", self.mview)
        assert self.type_ == b'PACK'

    def read_object(self, offset):
        """Return the content of a object at a offset.

        Arguments:
            offset: The offset to read from.

        Returns:
            bytes, bytes:

            A tuple (type, content) where:

             - type is the type of the object.
             - content is the content of the object (without header).
        """
        try:
            return self.__cache[offset]
        except KeyError:
            pass
        data = self.mview[offset:]
        header, data = read_ctypes(data, pack_first_obj_header)
        type_ = header.type
        size = header.size
        if header.cont:
            delta = 4
            header, data = read_ctypes(data, pack_other_obj_header)
            size += (header.size << delta)
            while header.cont:
                delta += 7
                header, data = read_ctypes(data, pack_other_obj_header)
                size += (header.size << delta)
        if type_ in (1, 2, 3, 4):
            out = decompress(data)
            assert size == len(out)
            self.__cache[offset] = ret = ObjectType(typeName[type_]), out
            return ret
        if type_ in (6, 7):
            if type_ == 6: # OBJ_OFS_DELTA
                header, data = read_ctypes(data, pack_other_obj_header)
                base_offset = header.size
                while header.cont:
                    base_offset += 1
                    header, data = read_ctypes(data, pack_other_obj_header)
                    base_offset =  (base_offset << 7) + header.size
                base_offset = offset - base_offset
            else: # OBJ_REF_DELTA
                base_offset, data = self.idxfile.get_offset(bytes(data[:20])), data[20:]

            delta_data = decompress(data)
            assert size == len(delta_data)
            typename, base = self.read_object(base_offset)
            data = apply_patch(base, delta_data)
            self.__cache[offset] = typename, data
            return typename, data


class index_header(ctypes.BigEndianStructure):
    _fields_ = [ ('magic'   , ctypes.c_uint8*4),
                 ('version' , ctypes.c_int32)
               ]

Fanouts = ctypes.c_int32*256

Sha = ctypes.c_uint8*20

Offset = ctypes.c_uint32

LongOffset = ctypes.c_uint64

class OffsetSha(ctypes.BigEndianStructure):
    _fields_ = [ ('offset', ctypes.c_uint32),
                 ('sha', ctypes.c_uint8*20)
               ]

class GitPackIndex:
    """A pack index

    Arguments:
            indexfile(path): The path of the index file.

    Methods:
        get_offset(sha): Return the offset in the pack associated to the sha.
    """
    def __init__(self, indexfile):
        self.indexfile = indexfile.open(mode='rb')
        self.mmap = mmap(self.indexfile.fileno(), 0, access=ACCESS_READ)
        self.mview = memoryview(self.mmap)
        header, _ = read_ctypes(self.mview, index_header)
        if bytes(header.magic) != b'\xfftOc':
            self.version = 1
        else:
            self.version = header.version

        self.readFanout()

        if self.version == 1:
            self.get_offset = self.get_offset1
            self.offsetshas = self.mview[256*4:256*4+24*self.nb_objects]
        else:
            self.get_offset = self.get_offset2
            self.shas = self.mview[258*4:258*4+20*self.nb_objects]
            self.offsets = self.mview[258*4+24*self.nb_objects:258*4+28*self.nb_objects]
            self.longOffsets = self.mview[258*4+28*self.nb_objects:]

    def close(self):
        if self.version == 1:
            self.offsetshas.release()
        else:
            self.shas.release()
            self.offsets.release()
            self.longOffsets.release()
        self.mview.release()
        self.mmap.close()
        self.indexfile.close()

    def __del__(self):
        self.close()
        self.indexfile = None

    def readFanout(self):
        fanouts, _ = read_ctypes(self.mview[0 if self.version==1 else 8:], Fanouts)
        self.fanouts = list(fanouts)

    @property
    def nb_objects(self):
        return self.fanouts[255]

    def get_offset1(self, sha):
        assert self.version == 1
        if sha[0]:
            startIndex = self.fanouts[sha[0]-1]
        else:
            startIndex = 0
        endIndex = self.fanouts[sha[0]]

        entries = self.offsetshas[24*startIndex:24*endIndex]
        _sha = None
        while len(entries):
            offset_sha, _ = read_ctypes(entries, OffsetSha)
            _sha = bytes(offset_sha.sha)
            assert sha[0] == _sha[0]
            if sha == _sha:
                return offset_sha.offset
            entries = entries[24:]
        raise KeyError

    def get_offset2(self, sha):
        assert self.version == 2
        if sha[0]:
            startIndex = self.fanouts[sha[0]-1]
        else:
            startIndex = 0
        endIndex = self.fanouts[sha[0]]

        _min, _max = startIndex, endIndex
        _sha = None
        _middle = None
        while _min != _max:
            _middle = (_min+_max)//2
            needStop = _min == _middle
            for a, b in zip(self.shas[20*_middle:], sha):
                if a<b:
                    #_sha is before what we search
                    _min = _middle
                    break
                if a>b:
                    #_sha is after what we search
                    _max = _middle
                    break
            else:
                # a==base
                startIndex = _middle
                break
            if needStop:
                raise KeyError
        else:
            raise KeyError

        offset, _ = read_ctypes(self.offsets[4*startIndex:], Offset)
        if offset & (1 << 31):
            offset -=  (1 << 31)
            offset, _ = read_ctypes(self.longOffsets[8*offset:], LongOffset)
        return offset


    def get_full_sha(self, value):
        if self.version == 1:
            entry_size = 24
            sha_read = lambda entries: bytes(read_ctypes(entries, OffsetSha)[0].sha)
            entries = self.offsetshas
        else:
            entry_size = 20
            sha_read = lambda entries: bytes(read_ctypes(entries, Sha)[0])
            entries = self.shas

        try:
            value = unhexlify(value.encode())
        except binasciiError:
            raise KeyError
        if value[0]:
            startIndex = self.fanouts[value[0]-1]
        else:
            startIndex = 0
        endIndex = self.fanouts[value[0]]

        entries = entries[entry_size*startIndex:entry_size*endIndex]
        found_start = found_end = None
        found_sha = _sha = None
        while len(entries):
            _sha = sha_read(entries)
            assert value[0] == _sha[0]
            if _sha.startswith(value):
                if found_sha:
                    # We've found two sha starting with value
                    raise KeyError
                found_sha = _sha
            elif found_sha:
                # the current sha do not start with value
                # but previous one does, return it
                return found_sha
            entries = entries[entry_size:]

        #end of the loop
        if found_sha:
            return found_sha

        raise KeyError
