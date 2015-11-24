# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""Read information in Postgresql system catalog

"""
from psycopg2.extensions import AsIs


class ColumnDoesNotExists(Exception):
    """A column does not exists

    Raised when a column is specificaly requested as a parameter in a
    function
    """
    pass


class TableDoesNotExists(Exception):
    """A table does not exists

    Raised when a table is specificaly requested as a parameter in a
    function
    """
    pass


class SchemaDoesNotExists(Exception):
    """A schema does not exists

    Raised when a schema is specificaly requested as a parameter in a
    function
    """
    pass


class PygCatalog(object):
    """Python library to read PostgreSQL system catalog

    """

    def __init__(self, conn=None, default_schemas=['public']):
        self.conn = conn
        self.tables = None
        self.indexes = {}
        self.lastquery = None
        self.default_schemas = default_schemas

    def _read_db(self, schema='public'):
        if self.tables is None:
            self.get_tables(schema=schema)

    def set_default_schema(self, schema):
        """Define the default schema to work on

        :param schema: The schema's name to work on
        :type schema: string

        :return: The result of the addition
        :rtype: boolean
        """
        if not isinstance(schema, str):
            raise ValueError

        self.default_schemas = [schema]
        return self.default_schemas

    def set_default_schemas(self, schemas):
        """Define as set of schemas to work on

        Remove schemas set twice or more
        """
        if not isinstance(schemas, list):
            raise ValueError

        def_schemas = []
        for schema in list(set(schemas)):
            def_schemas.append(self.set_default_schema(schema)[0])

        self.default_schemas = def_schemas

    def reset_cache(self):
        """Reset the cache
        """
        self.tables = None
        self.lastquery = None

    def analyze(self, table=None):
        """Run an ANALYZE over the database or a table
        """
        cur = self.conn.cursor()

        if table:
            qry = """ANALYZE %s"""
        else:
            qry = """ANALYZE"""

        return cur.execute(qry, (AsIs(table), ))

    def pgversion(self):
        """Run the version of PostgreSQL
        """
        cur = self.conn.cursor()
        qry = "SELECT version()"
        cur.execute(qry)
        return cur.fetchone()[0]

    def get_tables(self, **kwargs):
        """Return tables list

        You may specify a single schema to look in by specifying the
        keyword argumeent `schema`

        :Example:

        >>> cat.get_tables(schema='public')

        """
        qry = """
              SELECT c.relname, c.reltuples::bigint, c.oid, n.nspname
              FROM pg_class AS c
              INNER JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
              WHERE relkind = 'r'
              AND n.nspname IN %s
              """

        rows = self._execute_sql(qry, (self._which_schemas(**kwargs),))

        self.tables = {}
        for row in rows:
            self.tables[row[0]] = {'tuple': row[1],
                                   'oid': row[2],
                                   'schema': row[3],
                                   'columns': None}

        return self.tables

    def schemas(self):
        """Return schemas

        Return the list of all schemas present in the database

        :Example:

        >>> cat.get_schemas()
        ['pg_toast', 'pg_temp_1', 'pg_toast_temp_1', 'pg_catalog', 'public', 'information_schema', 'alice']

        :rtype: list
        """
        qry = """
              SELECT nspname
              FROM pg_catalog.pg_namespace
              """

        return [row[0] for row in self._execute_sql(qry)]

    def _which_schemas(self, **kwargs):
        if kwargs.get('schema'):
            return (kwargs['schema'],)
        else:
            return tuple(self.default_schemas)

    def table_tuples(self, table, **kwargs):
        """Return the table's number of tuples


        """
        schemas = self._which_schemas(**kwargs)

        qry = """
              SELECT c.relname, c.reltuples::bigint, n.nspname
              FROM pg_class AS c
              INNER JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
              WHERE relkind = 'r'
              AND c.relname = %s
              AND n.nspname IN %s
              """

        rows = self._execute_sql(qry, (table, schemas, ))

        row = rows[0]

        if row is None:
            raise TableDoesNotExists

        return row

    def biggest_tables(self, max=1, **kwargs):
        """Return the biggest table in term of total size

        The size is compute all disk usage used by the table, it
        includes datas, indexes and TOAST data.

        :Example:
        >>> cat.biggest_table()
        ('foo', 163840L, 1000L)
        """
        schemas = self._which_schemas(**kwargs)

        qry = """
              SELECT c.relname::text, n.nspname::text,
              pg_total_relation_size(c.relname::text),
              c.reltuples::bigint
              FROM pg_class AS c
              INNER JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
              WHERE c.relkind = 'r'
              AND n.nspname IN %s
              ORDER BY 2 DESC
              LIMIT %s
              """

        rows = self._execute_sql(qry, (schemas, max))
        return rows

    def biggest_table(self):
        """Return the biggest table in term of total size

        The size is compute all disk usage used by the table, it
        includes datas, indexes and TOAST data. Sizes are express in Bytes.

        :Example:
        >>> cat.biggest_table()
        ('foo', 163840L, 1000L)
        """
        rows = self.biggest_tables()

        return rows[0]

    def get_table_columns(self, table, schema='public'):
        """Return all columns in a table

        :rtype: list
        """
        self._read_db(schema=schema)

        if self.tables.get(table):
            return self._get_columns(self.tables[table]['oid'])
        else:
            return None

    def _get_columns(self, oid):
        """Return columns for a table
        """
        cur = self.conn.cursor()

        qry = """
              SELECT attname, attnum
              FROM pg_catalog.pg_attribute AS a
              WHERE attrelid = %s
              AND attnum > 0
              AND attisdropped = false
              """

        cur.execute(qry, (oid, ))
        columns = []
        for row in cur.fetchall():
            columns.append(row[0])

        return columns

    def _get_columns_extended(self, table_name, schema_name):
        """Return columns for a table
        """
        cur = self.conn.cursor()

        qry = """
              SELECT column_name, data_type, is_nullable::text, column_default,
              ordinal_position
              FROM information_schema.columns
              WHERE table_schema = %s
              AND table_name = %s
              ORDER BY ordinal_position
              """

        cur.execute(qry, (schema_name, table_name))
        columns = []
        for row in cur.fetchall():
            columns.append({'name': row[0],
                            'type': row[1],
                            'is_nullable': row[2],
                            'default_value': row[3],
                            'ordinal_position': row[4]})

        return columns

    def _execute_sql(self, qry, parms=None):
        """Execute a sql query
        """
        cur = self.conn.cursor()

        self.lastquery = cur.mogrify(qry, parms)

        cur.execute(qry, parms)

        return cur.fetchall()

    def get_indexes(self, schema='public', **kwargs):
        """Return all indexes in a schema

        Return all indexes defined in the schemas, each indexex is
        associated with the table oid, it's own oid, the number of
        tuples present in it and the name of the columns.

        :Example:

        >>> cat.get_indexes()
        {'foo_name_idx': {'table_oid': 121090,
                          'oid': 121093,
                          'columns': None,
                          'tuple': 1000L},
         'foo_name_ratio_idx': {'table_oid': 121090,
                                'oid': 121094,
                                'columns': None,
                                'tuple': 1000L}
        }

        :return: dict that contains all indexes
        :rtype: dict

        """
        qry = """
              SELECT c.relname, c.reltuples::bigint, c.oid, i.indrelid,
              i.indkey, i.indisunique, i.indclass, a.amname
              FROM pg_catalog.pg_class AS c
              INNER JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
              INNER JOIN pg_catalog.pg_index i ON c.oid = i.indexrelid
              INNER JOIN pg_catalog.pg_am a ON a.oid = c.relam
              WHERE c.relkind = 'i'
              AND n.nspname = %s
              """

        params = [schema]

        if kwargs.get('table'):
            qry = qry + "AND i.indrelid = %s"
            params.append(self._table_oid(kwargs.get('table'), schema))

        qry = qry + " ORDER BY c.relname"

        rows = self._execute_sql(qry, tuple(params))

        indexes = {}

        for row in rows:
            indcols = row[4].split(' ')
            cols = []
            if kwargs.get('table'):
                for col in self._get_columns_extended(kwargs.get('table'), schema):
                    if str(col['ordinal_position']) in indcols:
                        cols.append(col['name'])

            indexes[row[0]] = {'tuple': row[1],
                               'oid': row[2],
                               'columns': cols,
                               'table_oid': row[3],
                               'access_method': row[7],
                               'is_unique': row[5]}
        return indexes

    def get_operator_class(self, **kwargs):
        """Return information on oeprator class

        http://www.postgresql.org/docs/current/static/catalog-pg-opclass.html

        """
        qry = """
              SELECT oid, opcname
              FROM pg_catalog.pg_opclass
              """

        params = []

        if kwargs.get('oid'):
            qry = qry + "WHERE oid = %s"
            params.append(kwargs.get('oid'))

        rows = self._execute_sql(qry, tuple(params))

        operators = []
        for row in rows:
            operators.append({'oid': row[0],
                              'name': row[1]})

        return operators


    def get_triggers(self, tablename, **kwargs):
        """Return information on triggers

        http://www.postgresql.org/docs/current/static/catalog-pg-trigger.html

        :Example:

        >>> cat.get_triggers('foobar')
        [{'name': 'car_insert_trigger','event': 'INSERT'
          'timing', 'BEFORE'},
         {'name': 'car_update_trigger','event': 'UPDATE',
          'timing': 'AFTER'}
        ]

        :return: all triggers on a table
        :rtype: array

        """
        qry = """
              SELECT trigger_name, event_manipulation, action_timing
              FROM information_schema.triggers
              WHERE event_object_table = %s
              """

        rows = self._execute_sql(qry, (tablename,))

        triggers = []
        for row in rows:
            triggers.append({'name': row[0],
                             'event': row[1],
                             'timing': row[2]})

        return triggers

    def is_column_indexed(self, column_name, table_name, schema='public'):
        """Check if a column is indexed

        Check if the column is present in at least one index.

        :param column_name: The column's name to look for
        :param table_name: The table's name to look in
        :type column_name: string
        :type table_name: string
        :return: The result of the addition
        :rtype: boolean

        :Example:

        >>> is_table_exists('foobar')
        true
        """

        if not self.is_table_exists(table_name, schema):
            msg = "table %s does not exist in schema%s"
            raise TableDoesNotExists(msg % (schema, table_name))

        if not self.is_column_exists(column_name, table_name, schema):
            msg = "column %s does not exist in table %s.%s"
            raise ColumnDoesNotExists(msg % (column_name, schema, table_name))

        qry = """
        WITH cte AS (
        SELECT c.relname as indexname, c.oid, i.indrelid,
        unnest( i.indkey) as attnum

        FROM pg_class AS c

        INNER JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
        INNER JOIN pg_catalog.pg_index i ON c.oid = i.indexrelid

        WHERE c.relkind = 'i'
        AND n.nspname = %s
        )

        SELECT cte.*, a.attname, t.relname as tablename
        FROM cte
        INNER JOIN pg_class t ON cte.indrelid = t.oid
        INNER JOIN pg_catalog.pg_attribute a
        ON (cte.attnum = a.attnum AND a.attrelid = cte.indrelid)
        WHERE a.attname = %s AND t.relname = %s
        """

        rows = self._execute_sql(qry, (schema, column_name, table_name))

        return (len(rows) > 0)

    def is_column_exists(self, column_name, table_name, schema='public'):
        """Check if a column exists in a table

        :param column_name: the column's name to look for
        :param table_name: the table's name to look in

        """
        qry = """
        SELECT 1
        FROM pg_catalog.pg_attribute a
        INNER JOIN pg_class t ON a.attrelid = t.oid
        INNER JOIN pg_catalog.pg_namespace n ON t.relnamespace = n.oid
        WHERE n.nspname = %s
        AND a.attname = %s
        AND t.relname = %s
        """

        rows = self._execute_sql(qry, (schema, column_name, table_name))

        return (len(rows) > 0)

    def is_table_exists(self, table_name, schema='public'):
        """Check if a table exists

        :param table_name: The table's name to look for
        :type table_name: string
        :return: The result of the addition
        :rtype: boolean

        :Example:

        >>> is_table_exists('foobar')
        true
        """

        qry = """
        SELECT 1
        FROM pg_class t
        INNER JOIN pg_catalog.pg_namespace n ON t.relnamespace = n.oid
        WHERE n.nspname = %s
        AND t.relname = %s
        """
        rows = self._execute_sql(qry, (schema, table_name))

        return (len(rows) > 0)

    def _table_oid(self, table_name, schema='public'):
        """Return the table's oid

        :param table_name: The table's name to look for
        :type table_name: string
        :return: The result of the addition
        :rtype: boolean

        :Example:

        >>> _table_oid('foobar', schema='public')
        1241
        """

        qry = """
        SELECT t.oid
        FROM pg_class t
        INNER JOIN pg_catalog.pg_namespace n ON t.relnamespace = n.oid
        WHERE n.nspname = %s
        AND t.relname = %s
        """
        rows = self._execute_sql(qry, (schema, table_name))

        return rows[0][0]
