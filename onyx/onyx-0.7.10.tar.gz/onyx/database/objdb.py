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
from onyx.database.ufo_base import SPECIAL, custom_encoder, custom_decoder

import onyx.database as onyx_db

import psycopg2 as psql
import psycopg2.extras as psql_extras
import psycopg2.extensions as psql_ext
import psycopg2.errorcodes as psql_err
import pickle
import json
import abc

__all__ = ["ObjNotFound", "ObjDbError", "ObjExists", "ObjDbClient"]

# --- here we define standard query strings and error messages

QUERY_CLS_INSERT = "INSERT INTO ClassDefinitions VALUES (%s,%s);"
QUERY_CLS_GET = """
SELECT ClassDef FROM ClassDefinitions WHERE ObjType=%s;"""
QUERY_CLS_DELETE = """
DELETE FROM ClassDefinitions row WHERE row.ObjType=%s AND NOT
EXISTS (SELECT 1 FROM Objects WHERE ObjType=row.ObjType);"""

QUERY_OBJ_INSERT = "INSERT INTO Objects VALUES (%s,%s,%s,%s,%s,%s,%s);"
QUERY_OBJ_GET = "SELECT * FROM Objects WHERE Name=%s;"
QUERY_OBJ_UPDATE = """
UPDATE Objects
SET Version=%s, ChangedBy=%s, LastUpdated=%s, Data=%s
WHERE Name=%s AND Version=%s;"""
QUERY_OBJ_DELETE = "SELECT delete_obj(%s, %s) AS deleted;"
QUERY_OBJ_VERSION = "SELECT Version FROM Objects WHERE Name=%s LIMIT 1;"
QUERY_OBJ_EXISTS = """
SELECT EXISTS (SELECT 1 FROM Objects WHERE Name=%s) AS "exists";"""

QUERY_ARC_INSERT = "INSERT INTO Archive VALUES (%s,%s,%s,%s,%s,%s);"
QUERY_ARC_UPDATE = """
UPDATE Archive
SET ChangedBy=%s, TimeStamp=%s, Value=%s
WHERE Name=%s AND Attribute=%s AND Date=%s;"""
QUERY_ARC_GET = """
SELECT Value, Date FROM Archive
WHERE Name=%s AND Attribute=%s AND Date IN
    (SELECT MAX(Date) FROM Archive
     WHERE Name=%s AND Attribute=%s AND Date<=%s);"""
QUERY_ARC_GET_STRICT = """
SELECT Value, Date FROM Archive
WHERE Name=%s AND Attribute=%s AND Date=%s;"""

MSG_RELOAD = """
Instance of {0:s} is older (v.{1:d}) than the most recent version in database
(v.{2:d}): reload object from database before updating"""


###############################################################################
class ObjNotFound(Exception):
    pass


###############################################################################
class ObjDbError(Exception):
    pass


###############################################################################
class ObjExists(ObjDbError):
    pass


###############################################################################
class dummy_conn(object):
    """
    This is a dummy connection class that implements placeholders methods
    used to support transactions. It is used by the base and dummy clients
    and should not be used by production implementations.
    """
    def set_isolation_level(self, *args):
        pass

    def tpc_begin(self, *args):
        pass

    def tpc_commit(self, *args):
        pass

    def tpc_rollback(self, *args):
        pass


###############################################################################
class ObjDbBase(object):
    """
    Base class for ObjDb clients.
    """
    # -------------------------------------------------------------------------
    def __init__(self, database, user, host=None):
        self.dbname = database
        self.user = user
        self.host = host

        # --- lookup dictionary for class definitions
        self.class_defs = {}

        # --- the connection to the db-backend
        self.conn = dummy_conn()

        # --- store current transaction name
        self.transaction = None

    # -------------------------------------------------------------------------
    def class_lookup(self, cls_name):
        """
        Lookup class by class name.
        """
        return self.class_defs[cls_name]

    # -------------------------------------------------------------------------
    #  implements methods to retrieve, add and remove items from db-cache

    def __getitem__(self, name):
        return onyx_db.obj_instances[name]

    def __setitem__(self, name, instance):
        onyx_db.obj_instances[name] = instance

    def __delitem__(self, name):
        try:
            del onyx_db.obj_instances[name]
        except KeyError:
            pass

    # -------------------------------------------------------------------------
    #  method to test if an object exists in database. the base class
    #  implementation only checks if a reference exsists without testing the
    #  backend.
    def __contains__(self, name):
        return name in onyx_db.obj_instances

    # -------------------------------------------------------------------------
    @abc.abstractmethod
    def initialize(self):
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    @abc.abstractmethod
    def restart(self):
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    @abc.abstractmethod
    def close(self):
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    @abc.abstractmethod
    def add(self, obj):
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    @abc.abstractmethod
    def get(self, name, refresh=False):
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    @abc.abstractmethod
    def update(self, obj):
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    @abc.abstractmethod
    def delete(self, obj):
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    @abc.abstractmethod
    def set_dated(self, name, attr, date, value, overwrite=False):
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    @abc.abstractmethod
    def get_dated(self, name, attr, date, strict=False):
        raise NotImplementedError()


# -----------------------------------------------------------------------------
def typecast_to_Date(value, curs):
    if value is None:
        return None
    else:
        # --- maybe we should use a regexp like r"^.*'(.*)'.*$" ???
        return Date.parse(value)


###############################################################################
class ObjDbClient(ObjDbBase):
    core_tables = ("ClassDefinitions", "Objects", "Archive")

    # -------------------------------------------------------------------------
    def __init__(self, database, user, host=None, check=True):
        """
        Description:
            ObjDb database, client class. It exposes a minimal api.
        """
        super().__init__(database, user, host)

        # --- open database connection
        self.conn = psql.connect(host=host, database=database, user=user,
                                 cursor_factory=psql_extras.NamedTupleCursor)
        self.conn.set_isolation_level(psql_ext.ISOLATION_LEVEL_AUTOCOMMIT)

        # --- register typecast to Date for date, timpestamp, timestamptz
        curs = self.conn.cursor()
        curs.execute("SELECT NULL::date, NULL::timestamp, NULL::timestamptz;")
        oids = tuple([col.type_code for col in curs.description])
        psql_ext.register_type(psql_ext.new_type(oids, "Date",
                                                 typecast_to_Date))

        # --- register a no-op loads() function to turn-off automatic parsing
        #     of json/jsonb datatype
        psql_extras.register_default_json(loads=lambda x: x)
        psql_extras.register_default_jsonb(loads=lambda x: x)

        # --- validation: without the following tables in the backend the
        #                 client doesn't work properly.
        if check:
            curs = self.conn.cursor()
            for table in self.core_tables:
                try:
                    curs.execute("SELECT 1 FROM {0:s} LIMIT 1;".format(table))
                except psql.ProgrammingError:
                    raise RuntimeError("Table {0!s} is missing on "
                                       "{1!s}".format(table, self.dbname))

    # -------------------------------------------------------------------------
    def initialize(self):
        curs = self.conn.cursor()
        curs.execute("""
-- this table is used to lookup class definition from class name
CREATE TABLE
ClassDefinitions (
    ObjType  varchar(64) PRIMARY KEY,
    ClassDef bytea       NOT NULL );

-- this table is used to store UFO objects
CREATE TABLE
Objects (
    Name        varchar(64) PRIMARY KEY,
    ObjType     varchar(64) REFERENCES ClassDefinitions,
    Version     integer     NOT NULL,
    ChangedBy   varchar(64) NOT NULL,
    TimeCreated timestamptz NOT NULL,
    LastUpdated timestamptz NOT NULL,
    Data        jsonb       NOT NULL );

CREATE INDEX objects_objtype_idx ON Objects (ObjType);

-- this table is used to store archived (i.e. dated) attributes
CREATE TABLE
Archive (
    Name      varchar(64) REFERENCES Objects,
    Attribute varchar(64) NOT NULL,
    Date      date        NOT NULL,
    Value     jsonb       NOT NULL,
    ChangedBy varchar(64) NOT NULL,
    TimeStamp timestamptz NOT NULL,
    CONSTRAINT name_date UNIQUE (Name, Attribute, Date) );

CREATE INDEX archive_name_attr_idx ON Archive (Name, Attribute);

-- store procedure for deleting objects
CREATE OR REPLACE FUNCTION delete_obj(character varying, integer)
RETURNS boolean AS $$
DECLARE
    deleted record;
    remaining record;
BEGIN
    DELETE FROM Objects
    WHERE Name=$1 AND Version=$2
    RETURNING Name, ObjType INTO STRICT deleted;

    EXECUTE format('SELECT * FROM Objects
                    WHERE ObjType=$1 AND Name<>$2 LIMIT 1')
    INTO remaining
    USING deleted.ObjType, deleted.Name;

    IF NOT FOUND THEN
        EXECUTE format('DELETE FROM ClassDefinitions WHERE ObjType=$1;')
        USING deleted.ObjType;
    END IF;

    RETURN true;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE EXCEPTION 'object %, version % not found', $1, $2;
END;
$$ LANGUAGE plpgsql;""")

    # -------------------------------------------------------------------------
    def class_lookup(self, cls_name):
        try:
            return self.class_defs[cls_name]
        except KeyError:
            curs = self.conn.cursor()
            curs.execute(QUERY_CLS_GET, (cls_name,))
            row = curs.fetchone()
            if row is None:
                raise KeyError("Class definition unavailable for"
                               "{0!s} in {1!s}".format(cls_name, self.dbname))
            else:
                cls = pickle.loads(bytes(row[0]))
                self.class_defs[cls_name] = cls
                return cls

    # -------------------------------------------------------------------------
    def __contains__(self, name):
        if name in onyx_db.obj_instances:
            return True
        curs = self.conn.cursor()
        curs.execute(QUERY_OBJ_EXISTS, (name,))
        return curs.fetchone().exists

    # -------------------------------------------------------------------------
    def restart(self):
        self.close()
        self.conn = psql.connect(host=self.host,
                                 database=self.dbname, user=self.user)
        self.conn.set_isolation_level(psql_ext.ISOLATION_LEVEL_AUTOCOMMIT)

    # -------------------------------------------------------------------------
    def close(self):
        if hasattr(self, "conn") and not self.conn.closed:
            self.conn.close()

    # -------------------------------------------------------------------------
    def add(self, obj):
        # --- validate object's Name
        if not isinstance(obj.Name, str):
            if obj.Name is None:
                raise ObjDbError("Cannot persist objects with undefined Name")
            else:
                raise ObjDbError("Name attribute must be "
                                 "a string: {0!s}".format(type(obj.Name)))

        with self.conn.cursor() as curs:
            # --- if class definition is missing, add it to the
            #     ClassDefinitions table
            try:
                cls = self.class_lookup(obj.ObjType)
            except KeyError:
                cls = psql.Binary(pickle.dumps(obj.__class__, protocol=-1))
                curs.execute(QUERY_CLS_INSERT, (obj.ObjType, cls))

            # --- update time-stamp and changed-by on the object
            obj.LastUpdated = Date.now()
            obj.ChangedBy = self.user.upper()

            # --- serialize object and create record
            record = (obj.Name, obj.ObjType, obj.Version, obj.ChangedBy,
                      obj.TimeCreated, obj.LastUpdated, obj.to_json())

            try:
                curs.execute(QUERY_OBJ_INSERT, record)
            except psql.IntegrityError as err:
                if psql_err.lookup(err.pgcode) == "UNIQUE_VIOLATION":
                    raise ObjExists("Object {0!s} already in "
                                    "{1!s}".format(obj.Name, self.dbname))
                else:
                    raise ObjDbError("{0!s}. Name = "
                                     "{1!s}".format(err.message, obj.Name))

        self[obj.Name] = obj
        return obj

    # -------------------------------------------------------------------------
    def get(self, name, refresh=False):
        try:
            # --- if object must be retrieved from database raise exception and
            #     fall back
            if refresh:
                raise KeyError()
            # --- then try getting obj from database cache
            return self[name]
        except KeyError:
            # --- if not found in the db cache, get it from the database
            with self.conn.cursor() as curs:
                curs.execute(QUERY_OBJ_GET, (name,))
                row = curs.fetchone()

            if row is None:
                raise ObjNotFound("Object '{0!s}' not found "
                                  "in {1!s}".format(name, self.dbname))
            else:
                try:
                    obj = self[name]
                except KeyError:
                    cls = self.class_lookup(row.objtype)
                    self[name] = obj = cls.__new__(cls)

                for attr in SPECIAL:
                    setattr(obj, attr, getattr(row, attr.lower()))

                obj.from_json(row.data)

            return obj

    # -------------------------------------------------------------------------
    def update(self, obj):
        name = obj.Name

        # --- current version is used by the update query
        curr_ver = obj.Version

        # --- update time-stamp, changed-by and version on the object
        obj.LastUpdated = Date.now()
        obj.ChangedBy = self.user.upper()
        obj.Version += 1

        # --- serialize data and create record
        record = (obj.Version, obj.ChangedBy,
                  obj.LastUpdated, obj.to_json(), name, curr_ver)

        with self.conn.cursor() as curs:
            try:
                curs.execute(QUERY_OBJ_UPDATE, record)

                if curs.rowcount == 0:
                    # --- upadte failed: check why
                    curs.execute(QUERY_OBJ_VERSION, (name,))
                    res = curs.fetchone()

                    if res is None:
                        raise ObjNotFound("Object '{0!s}' not found in "
                                          "{1!s}".format(name, self.dbname))

                    if curr_ver < res.version:
                        msg = MSG_RELOAD.format(name, curr_ver, res.version)
                        raise ObjDbError(msg)

            except psql.IntegrityError as err:
                raise ObjDbError("{0!s}. Name = "
                                 "{1!s}".format(err.message, name))

        return obj

    # -------------------------------------------------------------------------
    def delete(self, obj):
        # --- call the delete method if available
        if hasattr(obj, "delete"):
            obj.delete()

        try:
            curs = self.conn.cursor()

            try:
                curs.execute(QUERY_OBJ_DELETE, (obj.Name, obj.Version))
            except psql.InternalError:
                # --- delete failed: check why
                curs.execute(QUERY_OBJ_VERSION, (obj.Name,))
                res = curs.fetchone()

                if res is None:
                    raise ObjNotFound("Object '{0!s}' not found "
                                      "in {1!s}".format(obj.Name, self.dbname))
                elif obj.Version < res.version:
                    msg = MSG_RELOAD.format(obj.Name, obj.Version, res.version)
                    raise ObjDbError(msg)
                else:
                    raise ObjDbError("Deletion of {0!s} failed without "
                                     "an obvious cause...".format(obj.Name))
            finally:
                curs.close()

        finally:
            del self[obj.Name]

    # -------------------------------------------------------------------------
    def set_dated(self, name, attr, date, value, overwrite=False):
        if not isinstance(name, str):
            if name is None:
                raise ObjDbError("Cannot archived attributes of "
                                 "an instance with undefined Name")
            else:
                raise ObjDbError("Name attribute must be "
                                 "a string: {0!s}".format(type(name)))

        value = json.dumps(value, cls=custom_encoder)
        changed_by = self.user.upper()
        time_stamp = Date.now()
        record_id = (name, attr, date)

        with self.conn.cursor() as curs:

            # --- first we try adding a new dated record
            record = (name, attr, date, value, changed_by, time_stamp)

            try:
                curs.execute(QUERY_ARC_INSERT, record)
            except psql.IntegrityError as err:
                if psql_err.lookup(err.pgcode) == "UNIQUE_VIOLATION":
                    if overwrite:
                        # --- ignore exception and try updating instead
                        pass
                    else:
                        raise ObjDbError("Archived tuple {0!s} cannot "
                                         "be overwritten".format(record_id))
                else:
                    raise ObjDbError("{0!s}. Archived tuple = "
                                     "{1!s}".format(err.message, record_id))
            else:
                # --- everything fine, set cache and return
                self[record_id] = value
                return

            # --- record_id exists already, try updating it
            record = (value, changed_by, time_stamp, name, attr, date)

            try:
                curs.execute(QUERY_ARC_UPDATE, record)
            except psql.IntegrityError as err:
                raise ObjDbError("{0!s}. Archived tuple = "
                                 "{1!s}".format(err.message, record_id))
            else:
                # --- everything fine, set cache and return
                self[record_id] = value
                return

    # -------------------------------------------------------------------------
    def get_dated(self, name, attr, date, strict=False):

        record_id = (name, attr, date)

        try:
            # --- first try getting the value from database cache
            return date, self[record_id]
        except KeyError:
            if strict:
                query = QUERY_ARC_GET_STRICT
                parms = (name, attr, date)
            else:
                query = QUERY_ARC_GET
                parms = (name, name, date)

            with self.conn.cursor() as curs:
                curs.execute(query, parms)
                row = curs.fetchone()

            if row is None:
                raise ObjNotFound("Archived tuple {0!s} not found "
                                  "in {1!s}".format(record_id, self.dbname))

            if not strict:
                # --- make sure we return the actual archive date
                arc_date = Date.parse(row.date)

            self[record_id] = value = json.loads(row.value, cls=custom_decoder)

            if arc_date != date:
                # --- cache the value for the actual archive date too
                self[(name, attr, arc_date)] = value

            return arc_date, value


###############################################################################
class ObjDbDummyClient(ObjDbBase):
    """
    A dummy client that never queries the database backend.
    """
    # -------------------------------------------------------------------------
    def restart(self):
        pass

    # -------------------------------------------------------------------------
    def close(self):
        pass

    # -------------------------------------------------------------------------
    def add(self, obj):
        if obj.Name in self:
            raise ObjExists("Object {0!s} already "
                            "in {1!s}".format(obj.Name, self.dbname))
        self[obj.Name] = obj
        return obj

    # -------------------------------------------------------------------------
    def get(self, name, refresh=False):
        if refresh:
            raise ObjDbError("get method of "
                             "ObjDbDummyClient does not support refresh")
        try:
            return self[name]
        except KeyError:
            raise ObjNotFound("Object '{0!s}' "
                              "not found in {1!s}".format(name, self.dbname))

    # -------------------------------------------------------------------------
    def update(self, obj):
        try:
            self[obj.Name] = obj
        except KeyError:
            raise ObjNotFound("Object '{0!s}' not "
                              "found in {1!s}".format(obj.Name, self.dbname))
        return obj

    # -------------------------------------------------------------------------
    def delete(self, obj):
        if hasattr(obj, "delete"):
            obj.delete()
        del self[obj.Name]

    # -------------------------------------------------------------------------
    def set_dated(self, name, attr, date, value, overwrite=False):
        self[(name, attr, date)] = value

    # -------------------------------------------------------------------------
    def get_dated(self, name, attr, date, strict=False):
        try:
            return date, self[(name, attr, date)]
        except KeyError:
            raise ObjNotFound("Archived tuple {0!s} not found in "
                              "{1!s}".format((name, attr, date), self.dbname))
