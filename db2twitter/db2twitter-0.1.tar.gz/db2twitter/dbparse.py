# -*- coding: utf-8 -*-
# Copyright © 2015 Carl Chenet <carl.chenet@ohmytux.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/

# DbParse class
'''DbParse class'''

from sqlalchemy import *
from sqlalchemy.orm import create_session
from sqlalchemy.ext.declarative import declarative_base

class DbParse(object):
    '''DbParse class'''
    def __init__(self, cfgvalues):
        '''Constructor of the DbParse class'''
        self.mainid = ''
        #Create and engine and get the metadata
        Base = declarative_base()
        engine = create_engine('{}://{}:{}@{}/{}'.format(cfgvalues['dbconnector'],
            cfgvalues['dbuser'],
            cfgvalues['dbpass'],
            cfgvalues['dbhost'], 
            cfgvalues['database']))
        #metadata = MetaData(bind=engine)
        meta = MetaData()
        meta.reflect(bind=engine)
        #dbtables = cfgvalues['dbtables'].split(',')
        #dbtables = [i for i in  dbtables if i != '']
        
        tableobjects = []
        tableschemas = {}
        #for table in dbtables:
        for table in cfgvalues['rows']:
            tableschemas[table] = Table(table, meta, autoload=True, autoload_with=engine)

        #Create a session to use the tables    
        session = create_session(bind=engine)

        self.allfields = []
        for table in cfgvalues['rows']:
            if not cfgvalues['ids']:
                tableobj = session.query(tableschemas[table]).order_by(tableschemas[table].columns.id.desc()).first()
            else:
                tabrequest = '{}'.format(cfgvalues['ids'][table])
                #tableobj = session.query(tableschemas[table]).order_by(getattr(tableschemas[table], tabrequest)).first()
                tableobj = session.query(tableschemas[table]).order_by(getattr(tableschemas[table].columns, tabrequest).desc()).first()

            # split the different fields we need
            self.allfields = self.allfields + [getattr(tableobj, i) for i in cfgvalues['rows'][table]]

    @property
    def dbvalues(self):
        '''Database parsed values'''
        return self.allfields
