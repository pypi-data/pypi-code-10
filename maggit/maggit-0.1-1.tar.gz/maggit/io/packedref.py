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

from binascii import unhexlify

def _packed_ref_parse_lines(lines):
    refs = []
    current = None
    for l in lines:
        if l.endswith(b'\n'):
            l = l[:-1]
        if l.startswith(b'#'):
            # We do not change our behavior base on the header for now.
            # Just ignore it
            continue
        try:
            sha, ref = l.split(b' ')
            sha = unhexlify(sha)
            # This is a new ref
            if current:
                refs.append(current)
            current = (ref, sha, None)
        except ValueError:
            if l.startswith(b'^'):
                current = current[0], current[1], unhexlify(l[1:])

    if current:
        refs.append(current)
    return refs

def packed_ref_parse(filename):
    """Parse a packed ref file.

    Arguments:
        filename(path): The path of the packed ref.

    Returns:
        List[Tuple[bytes, bytes, bytes]]:

        A list of (ref, sha, peeledsha) where:

         - ref is name of the ref
         - sha is the associated sha
         - peeledsha is the peeled sha associated to the ref if present. Else None.
    """
    try:
        with open(str(filename), 'rb') as f:
            return _packed_ref_parse_lines(f.readlines())
    except FileNotFoundError:
        return set()
