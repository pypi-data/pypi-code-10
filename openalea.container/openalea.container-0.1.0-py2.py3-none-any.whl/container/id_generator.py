# -*- python -*-
# -*- coding: utf-8 -*-
#
#       IdGenerator : graph package
#
#       Copyright  or Copr. 2006 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Fred Theveny <theveny@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       VPlants WebSite : https://gforge.inria.fr/projects/vplants/
#
""" This module provide a generator for id numbers.
"""


class IdMaxGenerator(object):
    """Simple id generator based on returning an id
    always superior to the highest fetched id.
    """
    def __init__(self):
        self._id_max = None

        self.clear()

    def clear(self):
        """ Reset the generator.
        """
        self._id_max = 0

    def get_id(self, pid=None):
        """Generate a new id.

        args:
         - pid (int): potential id to use, if None (default) generate a new id
        """
        if pid is None:
            ret = self._id_max
            self._id_max += 1
            return ret
        else:
            if pid < self._id_max:
                raise IndexError("id %d already used" % pid)
            self._id_max = max(self._id_max, pid + 1)
            return pid

    def release_id(self, pid):
        """Mark the given id as available

        args:
         - pid (int): id to release
        """
        del pid


class IdSetGenerator(object):
    """Keep a set of available ids.
    """
    def __init__(self):
        self._id_max = None
        self._available_ids = set()

        self.clear()

    def clear(self):
        """ Reset the generator.
        """
        self._id_max = 0
        self._available_ids.clear()

    def get_id(self, pid=None):
        """Generate a new id.

        args:
         - pid (int): potential id to use, if None (default) generate a new id
        """
        if pid is None:
            if len(self._available_ids) == 0:
                ret = self._id_max
                self._id_max += 1
                return ret
            else:
                return self._available_ids.pop()
        else:
            if pid >= self._id_max:
                self._available_ids.update(xrange(self._id_max, pid))
                self._id_max = pid + 1
                return pid
            else:
                try:
                    self._available_ids.remove(pid)
                    return pid
                except KeyError:
                    raise IndexError("id %d already used" % pid)

    def release_id(self, pid):
        """Mark the given id as available

        args:
         - pid (int): id to release
        """
        if pid > self._id_max:
            raise IndexError("id out of range")
        elif pid in self._available_ids:
            raise IndexError("id currently not in use")
        else:
            self._available_ids.add(pid)


class IdGenerator(IdSetGenerator):
    """Alias to define a default id generator.
    """
    pass


class IdListGenerator(object):
    """Keep a list of unused ids instead of a set.
    """
    def __init__(self):
        self._id_max = None
        self._id_list = []

        self.clear()

    def clear(self):
        """ Reset the generator.
        """
        self._id_max = 0
        del self._id_list[:]

    def get_id(self, pid=None):
        if pid is None:
            if len(self._id_list) == 0:
                ret = self._id_max
                self._id_max += 1
                return ret
            else:
                return self._id_list.pop()
        else:
            if pid >= self._id_max:
                self._id_list.extend(range(self._id_max, pid))
                self._id_max = pid + 1
                return pid
            else:
                try:
                    ind = self._id_list.index(pid)
                    del self._id_list[ind]
                    return pid
                except ValueError:
                    raise IndexError("id %d already used" % pid)

    def release_id(self, pid):
        """Mark the given id as available

        args:
         - pid (int): id to release
        """
        if pid > self._id_max:
            raise IndexError("id out of range")
        elif pid in self._id_list:
            raise IndexError("id currently not in use")
        else:
            self._id_list.append(pid)
