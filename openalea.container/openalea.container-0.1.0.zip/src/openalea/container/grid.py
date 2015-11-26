# -*- python -*-
# -*- coding: utf-8 -*-
#
#       Grid : grid package
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
"""This module provide a simple pure python implementation
for a grid interface
"""


class Grid(object):
    """Interface definition of simple N dimensional grids
    with finite number of cell per dimension
    """

    def __init__(self, shape):
        """Constructor of a finite grid.

        args:
         - shape (iter of int): number of cell in each dimension
        """
        self._shape = [int(s) for s in shape]
        offset = [1]
        for i, incr in enumerate(self._shape[:-1]):
            offset.append(offset[i] * incr)
        self._offset = offset

    # ##########################################################
    #
    #               Grid concept
    #
    # ##########################################################
    def dim(self):
        """Dimension of the grid, i.e. number of axes.

        return:
         - (int)
        """
        return len(self._shape)

    def shape(self):
        """Shape of the grid, i.e. number of cell along each axis.

        return:
         - (iter of int)
        """
        return iter(self._shape)

    # ##########################################################
    #
    #               Cell list concept
    #
    # ##########################################################
    def __len__(self):
        """Total number of boxes in the grid.

        return:
         - (int)
        """
        if len(self._shape) == 0:
            return 0

        s = 1
        for incr in self._shape:
            s *= incr
        return s

    def __iter__(self):
        """Iterate on index of each cell in the grid.

        return:
         - (iter of int)
        """
        return iter(xrange(self.__len__()))

    def index(self, coord):
        """Compute the index of a cell from his position
        inverse function of `coordinates`

        args:
         - coord (tuple of int): position along each axis

        return:
         - (int)
        """
        ind = 0
        for i, offset in enumerate(self._offset):
            if not (0 <= coord[i] < self._shape[i]):
                msg = "coord (%d) along axis %d not valid" % (coord[i], i)
                raise IndexError(msg)

            ind += coord[i] * offset

        return ind

    def coordinates(self, ind):
        """Compute the position along each axis from the index of the cell.
        inverse function of `index`

        args:
         - ind (int): index of the cell

        return:
         - (tuple of int)
        """
        imax = len(self)
        if not (0 <= ind < imax):
            msg = "index out of range index: %d max : %d" % (ind, imax)
            raise IndexError(msg)

        residue = ind
        coord = []
        for i in xrange(self.dim() - 1, -1, -1):
            coord.append(residue / self._offset[i])
            residue %= self._offset[i]

        coord.reverse()

        return tuple(coord)
