#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Farfetch API
# Copyright (c) 2008-2015 Hive Solutions Lda.
#
# This file is part of Hive Farfetch API.
#
# Hive Farfetch API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Farfetch API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Farfetch API. If not, see <http://www.apache.org/licenses/>.

__author__ = "Rui Castro <rui.castro@gmail.com>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2015 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

class CountryApi(object):

    def list_countries(
        self,
        q = None,
        page = None,
        page_size = None,
        sort = None,
        filters = None
    ):
        page = page or 1
        page_size = page_size or 10
        find_s = q.get("find_s", "")
        find_l = find_s.lower()

        url = self.base_url + "countries"
        contents = self.get(url)

        countries = []
        for country in contents:
            name = country["name"]
            name_l = name.lower()
            if not name_l.startswith(find_l): continue
            countries.append(country)

        skip = (page - 1) * page_size
        countries = countries[skip:skip + page_size]
        return countries

    def get_country(self, id):
        url = self.base_url + "countries/%s" % id
        contents = self.get(url)
        return contents

    def country_states(self, id):
        url = self.base_url + "countries/%s/states" % id
        contents = self.get(url)
        return contents

    def country_currencies(self, id):
        url = self.base_url + "countries/%s/Currency" % id
        contents = self.get(url)
        return contents
