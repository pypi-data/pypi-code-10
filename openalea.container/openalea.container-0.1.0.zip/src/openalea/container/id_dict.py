# -*- python -*-
# -*- coding: utf-8 -*-
#
#       IdDict : container package
#
#       Copyright  or Copr. 2006 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       VPlants WebSite : https://gforge.inria.fr/projects/vplants/
#
"""This module provide a dictionary that create keys when needed.
"""

from id_generator import IdMaxGenerator, IdSetGenerator, IdListGenerator

IdGen = {"max": IdMaxGenerator,
         "set": IdSetGenerator,
         "list": IdListGenerator}


class IdDict(dict):
    """Store a tuple of (id,elm) like a normal dict
    Create an id to use as key when needed
    """

    def __init__(self, *args, **kwdargs):
        try:
            gen_name = kwdargs.pop("idgenerator")
        except KeyError:
            gen_name = "set"
        dict.__init__(self, *args, **kwdargs)

        self._id_generator = None
        self._init_id_generator(gen_name)

        for k in self.keys():
            self._id_generator.get_id(k)

    def _init_id_generator(self, gen_name='set'):
        try:
            self._id_generator = IdGen[gen_name]()
        except KeyError:
            msg = "the required id generator (%s) is unknown" % gen_name
            msg += "\navailable generator are %s" % str(IdGen.keys())
            raise UserWarning(msg)

    def get_generator_type(self):
        """Retrieve name of id generator used
        """
        for name, typevalue in IdGen.items():
            if type(self._id_generator) == typevalue:
                return name

    def add(self, val, key=None):
        """Insert a new value in the dict generating an id
        to use as key if needed.

        args:
         - val (any): value to store
         - key (int): key to use, if None (default) a new one will generated
        """
        try:
            key = self._id_generator.get_id(key)
            dict.__setitem__(self, key, val)
            return key
        except IndexError:
            raise KeyError(key)
        except TypeError:
            raise KeyError(key)

    def __deepcopy__(self, memo):
        from copy import deepcopy
        newobj = IdDict(idgenerator=self.get_generator_type())
        for key, val in self.iteritems():
            dict.__setitem__(newobj, deepcopy(key, memo), deepcopy(val, memo))
        newobj._id_generator = deepcopy(self._id_generator, memo)
        return newobj

    ################################################
    #
    #               dict interface
    #
    ################################################
    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self._id_generator.release_id(key)

    def __setitem__(self, key, val):
        if key not in self:
            # if not hasattr(self, '_id_generator'):  # TODO test this case
            #     self._init_id_generator()
            try:
                self._id_generator.get_id(key)
            except TypeError:
                raise KeyError
        dict.__setitem__(self, key, val)

    def clear(self):
        dict.clear(self)
        self._id_generator.clear()

    def copy(self):
        return IdDict(self)

    def pop(self, key, *args):
        try:
            val = dict.pop(self, key)
            self._id_generator.release_id(key)
            return val
        except KeyError:
            if len(args) > 0:
                return args[0]
            else:
                raise

    def popitem(self):
        key, val = dict.popitem(self)
        self._id_generator.release_id(key)
        return key, val

    def setdefault(self, key, *args):
        if key not in self:
            try:
                self._id_generator.get_id(key)
            except TypeError:
                raise KeyError
        return dict.setdefault(self, key, *args)

    def update(self, E=None, **F):
        raise NotImplementedError("lapin compris")
