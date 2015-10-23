#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Omni ERP
# Copyright (c) 2008-2015 Hive Solutions Lda.
#
# This file is part of Hive Omni ERP.
#
# Hive Omni ERP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Omni ERP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Omni ERP. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

from . import util

class MerchandiseApi(object):

    def list_merchandise(self, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/merchandise.json"
        contents = self.get(
            url,
            **kwargs
        )
        return contents

    def update_merchandise(self, id, payload):
        url = self.base_url + "omni/merchandise/%d/update.json" % id
        contents = self.post(url, data_m = payload)
        return contents

    def list_store_merchandise(self, store_id = None, *args, **kwargs):
        util.filter_args(kwargs)
        url = self.base_url + "omni/merchandise/store.json"
        contents = self.get(
            url,
            store_id = store_id,
            **kwargs
        )
        return contents

    def prices_merchandise(self, items):
        url = self.base_url + "omni/merchandise/prices.json"
        self.put(url, data_j = items)
