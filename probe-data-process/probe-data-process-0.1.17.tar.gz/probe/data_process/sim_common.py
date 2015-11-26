"""
.. module:: sim_process
   :platform: Unix
   :synopsis: A useful module indeed.

.. moduleauthor:: Petr Zikan <zikan.p@gmail.com>

This module contains just class SimCommon and logging setting.
SimCommon serves as a common ancestor of other Sim classes.
"""

from __future__ import absolute_import
import h5py
import logging

logger = logging.getLogger(__name__)

class SimCommon(object):
    """
    This is a simple "low-level" class that should contain all general
    functionality for manipulation with hdf5 files.

    It only stores filename as ``self.h5_filename``, then opens and stores
    a handle to hdf5 file as ``self.h5_f``.
    """

    def __init__(self, h5_filename):
        """
        Args:
            h5_filename (str): path to hdf5 file with results
        """

        self.h5_filename = h5_filename
        logger.debug('self.h5_filename: %s', self.h5_filename)

        self.h5_f = h5py.File(self.h5_filename, 'r+')


    def get_list_of_groups_as_dict(self, starts_with):
        """
        Args:
            starts_with (str): groups prefix

        Returns:
            dict - key is int of group number, value is group name

        """
        return {int(x.split('_')[1]): x for x in self.h5_f if x.startswith(starts_with)}


    def get_attrs_as_dict(self, group):
        """
        Returns dict with group's attributes.

        Args:
            group (str) - name of group (assumed group at /)
        Returns:
            dict - {attr_name: value}
        """
        return {a : v[0] for a, v in self.h5_f['/{}'.format(group)].attrs.iteritems()}

