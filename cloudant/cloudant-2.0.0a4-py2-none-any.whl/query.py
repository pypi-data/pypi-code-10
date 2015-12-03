#!/usr/bin/env python
# Copyright (c) 2015 IBM. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
API module for composing and executing Cloudant queries.
"""

import posixpath
import json
import types

from .account import Cloudant
from .errors import CloudantException, CloudantArgumentError

ARG_TYPES = {
    'selector': dict,
    'limit': (int, types.NoneType),
    'skip': (int, types.NoneType),
    'sort': list,
    'fields': list,
    'r': (int, types.NoneType),
    'bookmark': basestring,
    'use_index': basestring
}

class Query(dict):
    """
    Encapsulates a query as a dictionary based object.
    """

    def __init__(self, database, **kwargs):
        super(Query, self).__init__()
        self.database = database
        if not isinstance(self.database.cloudant_account, Cloudant):
            raise CloudantException(
                'Database must be a Cloudant database.  '
                'Check your database and try again.'
            )
        self._r_session = self.database.r_session
        self._encoder = self.database.cloudant_account.encoder
        super(Query, self).update(kwargs)

    @property
    def url(self):
        """
        Constructs and returns the Query URL.

        :returns: Query URL
        """
        return posixpath.join(self.database.database_url, '_find')

    def __call__(self, **kwargs):
        """
        blah
        """
        data = dict(self)
        data.update(kwargs)

        # Validate query arguments and values
        for key, val in data.iteritems():
            if key not in ARG_TYPES.keys():
                msg = 'Invalid argument: {0}'.format(key)
                raise CloudantArgumentError(msg)
            if not isinstance(val, ARG_TYPES[key]):
                msg = 'Argument {0} is not expected type: {1}'.format(
                    key,
                    ARG_TYPES[key]
                )
                raise CloudantArgumentError(msg)
        if data.get('selector', None) is None:
            msg = (
                'No selector in the query.  '
                'Add a selector to define the query and retry.'
            )
            raise CloudantArgumentError(msg)
        if data.get('fields', None) is None:
            msg = (
                'No fields list in the query.  '
                'Add a list of fields for the query and retry.'
            )
            raise CloudantArgumentError(msg)

        # Execute query find
        headers = {'Content-Type': 'application/json'}
        resp = self._r_session.post(
            self.url,
            headers=headers,
            data=json.dumps(data, cls=self._encoder)
        )
        resp.raise_for_status()
        return resp.json()
