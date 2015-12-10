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

_setattr = object.__setattr__

class Sha(bytes):
    """
    A Sha is a git sha. It means that it is the identifier of a git object.

    Sha are store in Maggit as a 20 bytes len.
    """
    def __new__(cls, unhexbytes, hexbytes=None, hexstr=None):
        instance = super(Sha, cls).__new__(cls, unhexbytes)
        _setattr(instance, '_hexbytes', hexbytes)
        _setattr(instance, '_hexstr', hexstr)
        return instance

    @property
    def hexbytes(self):
        """The sha as a hexlified bytes"""
        if self._hexbytes is None:
            _setattr(self, '_hexbytes', hexlify(self))
        return self._hexbytes

    @property
    def hexstr(self):
        """The sha as a hexlified str"""
        if self._hexstr is None:
            _setattr(self, '_hexstr', self.hexbytes.decode())
        return self._hexstr

    @staticmethod
    def __setattr__(name, value):
        raise RuntimeError("Cannot modify a constant object")

    def __str__(self):
        return self.hexstr

    def __repr__(self):
        return "<Sha %s>"%self

    @staticmethod
    def cast(other):
        return _castdict[type(other)](other)

    @staticmethod
    def from_bytes(value):
        if len(value) == 20:
            #unhexlified sha
            return Sha(value)
        if len(value) == 40:
            #hexlified sha
            return Sha(unhexlify(value), hexbytes=value)
        raise ValueError("%r is not a valid value for a Sha"%value)

    @staticmethod
    def from_str(value):
        if len(value) == 40:
            #hexlified sha
            return Sha(unhexlify(value.encode()), hexstr=value)
        if len(value) == 20:
            #unhexlified sha
            return Sha(value.encode())
        raise ValueError("%r is not a valid value for a Sha"%value)

_castdict = {
    Sha : lambda o : o,
    bytes : Sha.from_bytes,
    str   : Sha.from_str
}
