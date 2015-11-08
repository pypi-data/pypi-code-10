# -*- coding: utf-8 -*-
#
# Unsettings - a configuration frontend for the Unity desktop environment
#
# Copyright (C) 2012 Florian Diesch <devel@florian-diesch.de>
#
# Homepage: http://www.florian-diesch.de/software/unsettings/
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

import itertools

from zeitgeist.datamodel import Event, Subject
from zeitgeist.client import ZeitgeistClient

ALL_EVENTS = Event.new_for_values()
ID_BLOCK_ALL = 'block-all'

client = ZeitgeistClient()
blacklist = client._iface.get_extension('Blacklist', 
                                        'blacklist')
        
def zeitgeist_is_enabled():
    try:
        templates = blacklist.GetTemplates()
        return not any(itertools.imap(
            ALL_EVENTS.matches_template, 
            templates.itervalues())
        )
    except Exception as e:
        print "Error connecting Zeitgeist: %s"% e
        return False


def zeitgeist_enable():
    blacklist.RemoveTemplate(ID_BLOCK_ALL)

def zeitgeist_disable():
    blacklist.AddTemplate(ID_BLOCK_ALL, 
                          ALL_EVENTS)

def zeitgeist_clear_all():
    def callback(event_ids):
        client.delete_events(event_ids)
    client.find_event_ids_for_templates([ALL_EVENTS], 
                                        callback, num_events=0)


