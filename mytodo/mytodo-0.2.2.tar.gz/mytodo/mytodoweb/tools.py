#!/usr/bin/env python2
#Copyright (C) 2015 Mohamed Aziz knani

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>

from . import database

def checkuser(username, password):
  if username is None or password is None:
    return False
  s = database.Session()
  # Checks if the username exists
  found = s.query(database.User).filter_by(username = username).first()
  if found is None:
    return False

  if found.username != username or found.password != password:
    return False

  return True

def getOwnerbyUsername(username):
  s = database.Session()
  return s.query(database.User).filter_by(username = username).first().id
