#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Netius System
# Copyright (c) 2008-2015 Hive Solutions Lda.
#
# This file is part of Hive Netius System.
#
# Hive Netius System is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Netius System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Netius System. If not, see <http://www.apache.org/licenses/>.

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

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import os
import gzip

import netius.clients

class GeoResolver(object):

    DB_NAME = "GeoLite2-City.mmdb"
    """ The name of the file that contains the geo ip
    information database (to be used in execution) """

    DOWNLOAD_URL = "http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.mmdb.gz"
    """ The url to the compressed version of the geo ip
    city database used for resolution """

    _db = None
    """ The reference to the internal database reference object
    that is going to be used in the geo ip resolution """

    @classmethod
    def resolve(cls, address):
        db = cls._get_db()
        if not db: return None
        return db.get(address)

    @classmethod
    def _get_db(cls):
        if cls._db: return cls._db
        try: import maxminddb
        except: return None
        if not os.path.exists(cls.DB_NAME): cls._download_db()
        if not os.path.exists(cls.DB_NAME): return None
        cls._db = maxminddb.open_database(cls.DB_NAME)
        return cls._db

    @classmethod
    def _download_db(cls, path = DB_NAME):
        path_gz = path + ".gz"
        result = netius.clients.HTTPClient.method_s(
            "GET",
            cls.DOWNLOAD_URL,
            async = False
        )
        response = netius.clients.HTTPClient.to_response(result)
        contents = response.read()
        file = open(path_gz, "wb")
        try: file.write(contents)
        finally: file.close()
        file = gzip.open(path_gz, "rb")
        try: contents = file.read()
        finally: file.close()
        file = open(path, "wb")
        try: file.write(contents)
        finally: file.close()
        os.remove(path_gz)
        return path
