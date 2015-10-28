###############################################################################
#
#   Onyx Portfolio & Risk Management Framework
#
#   Copyright 2014 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from onyx.datatypes.date import Date
from onyx.datatypes.gcurve import GCurve
from onyx.datatypes.curve import Curve
from onyx.database.ufo_base import UfoBase, custom_decoder
from onyx.database.ufo_fields import FloatField
from onyx.database.objdb import ObjNotFound
from onyx.database.objdb_api import ObjDbQuery

import onyx.database as onyx_db
import json

__all__ = ["Archivable"]

GET_HISTORY_QUERY = """
SELECT Date, Value FROM Archive
WHERE Name=%s AND Attribute=%s AND Date BETWEEN %s AND %s ORDER BY Date;"""

GET_MOST_RECENT = """
SELECT MAX(Date) FROM Archive
WHERE Name=%s AND Attribute=%s AND Date <= %s"""


###############################################################################
class Archivable(UfoBase):
    """
    Base class for all archivable UFO objects.
    """

    # -------------------------------------------------------------------------
    def last_before(self, attr, date=None):
        """
        Description:
            Return the date of the most recent archived record before a given
            date.
        Inputs:
            attr - the required attribute
            date - look for dated records with date earlier than this value.
        Returns:
            A Date.
        """
        date = date or Date.high_date()
        res = ObjDbQuery(GET_MOST_RECENT,
                         (self.Name, attr, date), attr="fetchone")
        if res.max is None:
            raise ObjNotFound("{0!s} not found for any date earlier"
                              "than {1:s}".format((self.Name, attr), date))
        else:
            return res.max

    # -------------------------------------------------------------------------
    def get_dated(self, attr, date, strict=False):
        """
        Description:
            Get the value of an archived attribute as of a given date.
        Inputs:
            attr   - the attribute to archive
            date   - the archive date
            strict - if true, raise an ObjNotFound exception if a record cannot
                     be found for the required date
        Returns:
            A (Date, value) tuple
        """
        # --- get the instance of the field descriptor that is storing
        #     the attribute descriptor itself
        field = getattr(self.__class__, attr).field

        # --- load from database and de-serialize value
        date, value = onyx_db.obj_clt.get_dated(self.Name,
                                                attr, date, strict=strict)
        return date, field.from_json(value)

    # -------------------------------------------------------------------------
    def set_dated(self, attr, date, value, overwrite=False):
        """
        Description:
            Set the value of an archived attribute.
        Inputs:
            attr      - the attribute to archive
            date      - the archive date
            value     - the value to archive
            overwrite - if true, existing records can be overwritten
        """
        # --- get the instance of the field descriptor that is storing
        #     the attribute descriptor itself
        field = getattr(self.__class__, attr).field
        # --- make sure value is compatible with the field_type
        field.validate(value)
        # --- serialize value
        value = field.to_json(value)

        onyx_db.obj_clt.set_dated(self.Name, attr,
                                  date, value, overwrite=overwrite)

    # -------------------------------------------------------------------------
    def delete(self):
        """
        Invoked when the archived object is deleted from database.
        """
        ObjDbQuery("DELETE FROM Archive WHERE Name=%s", parms=(self.Name,))

    # -------------------------------------------------------------------------
    def get_history(self, attr, start=None, end=None):
        start = start or Date.low_date()
        end = end or Date.high_date()

        # --- get the instance of the field descriptor that is stored
        #     the VT descriptor itself
        field = getattr(self.__class__, attr).field

        parms = (self.Name, attr, start, end)
        rows = ObjDbQuery(GET_HISTORY_QUERY, parms, attr="fetchall")

        def convert(v):
            return field.from_json(json.loads(v, cls=custom_decoder))

        knots = [(Date.parse(r[0]), convert(r[1])) for r in rows]

        if isinstance(field, FloatField):
            return Curve([d for d, v in knots], [v for d, v in knots])
        else:
            return GCurve([d for d, v in knots], [v for d, v in knots])
