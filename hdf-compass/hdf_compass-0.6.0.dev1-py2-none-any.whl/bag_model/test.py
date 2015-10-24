##############################################################################
# Copyright by The HDF Group.                                                #
# All rights reserved.                                                       #
#                                                                            #
# This file is part of the HDF Compass Viewer. The full HDF Compass          #
# copyright notice, including terms governing use, modification, and         #
# terms governing use, modification, and redistribution, is contained in     #
# the file COPYING, which can be found at the root of the source code        #
# distribution tree.  If you do not have access to this file, you may        #
# request a copy from help@hdfgroup.org.                                     #
##############################################################################
from __future__ import absolute_import, division, print_function

import os

from hdf_compass.compass_model.test import store, container
from hdf_compass.bag_model import BAGGroup, BAGStore
from hdf_compass.utils import data_url

url = os.path.join(data_url(), "bag", "bdb_00.bag")

s = store(BAGStore, url)
c = container(BAGStore, url, BAGGroup, "/")