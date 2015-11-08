#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# Unsettings - A configuration frontend for the Unity desktop environment
# http://www.florian-diesch.de/software/unsettings/
#
# Copyright (C) 2014 Florian Diesch <devel@florian-diesch.de>
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os.path, sys

fullpath = os.path.abspath(__file__)
path = os.path.split(fullpath)[0]
sys.path=[path]+sys.path

import unsettings, unsettings.settings

DATA_DIR=os.path.normpath(os.path.join(path, 'data'))

unsettings.settings.DATA_DIR = DATA_DIR
unsettings.settings.UI_DIR = os.path.join(DATA_DIR, 'ui')
unsettings.settings.ICON_DIR = os.path.join(DATA_DIR, 'icons')
    

unsettings.main()
