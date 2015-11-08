#!/usr/bin/env python
#-*- coding: utf-8-*-
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


from gi.repository import Gtk, GLib
import gettext, locale
from gettext import gettext as _


def yes_no_cancel_question(parent, title, text):    
    dlg = Gtk.MessageDialog(parent, 0,  Gtk.MessageType.QUESTION,
                            Gtk.ButtonsType.NONE,
                            text
                            )
    dlg.set_title(title)
    dlg.add_buttons(
        Gtk.STOCK_YES, Gtk.ResponseType.YES,
        Gtk.STOCK_NO, Gtk.ResponseType.NO,
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,                    
        )
    result = dlg.run()
    dlg.destroy()
    return result

def confirmation(parent, text, title=_('Confirm')):
    dlg = Gtk.MessageDialog(parent, 0,  Gtk.MessageType.QUESTION,
                            Gtk.ButtonsType.NONE,
                            text
                            )
    dlg.set_title(title)
    dlg.add_buttons(
        Gtk.STOCK_YES, Gtk.ResponseType.YES,
        Gtk.STOCK_NO, Gtk.ResponseType.NO,
        )
    result = dlg.run()
    dlg.destroy()
    return result == Gtk.ResponseType.YES

def information(parent, title, text):    
    dlg = Gtk.MessageDialog(parent, 0,  Gtk.MessageType.INFO,
                            Gtk.ButtonsType.OK,
                            text
                            )
    dlg.set_title(title)
    result = dlg.run()
    dlg.destroy()
    return result    


def error(text):    
    dlg = Gtk.MessageDialog(None, 0,  Gtk.MessageType.ERROR,
                            Gtk.ButtonsType.OK,
                            text
                            )
    dlg.set_title(_('Error'))
    result = dlg.run()
    dlg.destroy()
    return result    


def ask_for_file_name(title, parent, 
                      action=Gtk.FileChooserAction.SAVE, 
                      default_ext=None, 
                      overwrite_confirmation=True,
                      filters=()):
    if action == Gtk.FileChooserAction.SAVE:
        ok_button = Gtk.STOCK_SAVE
    elif action == Gtk.FileChooserAction.OPEN:
        ok_button = Gtk.STOCK_OPEN
    else: # CREATE_FOLDER, SELECT_FOLDER
        ok_button = Gtk.STOCK_OPEN
    
    dialog = Gtk.FileChooserDialog(title, parent, action,
                                       (Gtk.STOCK_CANCEL, 
                                        Gtk.ResponseType.CANCEL,
                                        ok_button, 
                                        Gtk.ResponseType.OK))
    for name, ext in filters:
        filter = Gtk.FileFilter()
        filter.set_name(name)
        filter.add_pattern('*.%s'%ext)
        dialog.add_filter(filter)
        
    filter = Gtk.FileFilter()
    filter.set_name(_("Any files"))
    filter.add_pattern("*")
    dialog.add_filter(filter)
    
    dialog.set_do_overwrite_confirmation(overwrite_confirmation)
    response = dialog.run()
    path = dialog.get_filename()
    dialog.destroy()

    if response != Gtk.ResponseType.OK:
        return

    if  default_ext is not None and '.' not in path:
            path = '.'.join((path, default_ext))

    return path


def cleaning_dlg(func, text, explanation=None):
    dlg = Gtk.MessageDialog(None, 0,  Gtk.MessageType.WARNING,
                            Gtk.ButtonsType.NONE,
                            text
                            )
 
    dlg.set_title(_('Confirm'))    
    dlg.set_property('use-markup', True)
    dlg.add_buttons(
        Gtk.STOCK_OK, Gtk.ResponseType.OK,
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        )

    if explanation:
        box = dlg.get_message_area()
        expander = Gtk.Expander.new(_('What does this mean?'))
        label = Gtk.Label()
        label.set_markup(explanation)
        label.set_property('max-width-chars', 55)
        label.set_property('wrap', True)
        label.set_property('selectable', True)
        expander.add(label)
        expander.show_all()
        box.add(expander)

    result = dlg.run()
    dlg.destroy()
    if result != Gtk.ResponseType.OK:
        return
    

    #  Just to show we are doing something
    dlg = Gtk.MessageDialog(None, 0,  Gtk.MessageType.INFO,
                            Gtk.ButtonsType.NONE, _('Cleaning...'))
                            
    pbar = Gtk.ProgressBar()
    pbar.show()
    dlg.get_action_area().add(pbar)
    def pulse(*args):
        pbar.pulse()
        while Gtk.events_pending():
            Gtk.main_iteration()
        if dlg.get_visible():
            return True
        else:
            dlg.destroy()
            return False

    dlg.show()
    GLib.timeout_add(40, pulse)
    if func(): # an error occured: hide dlg
        timeout = 0
    else: # no error: visible at least 1 second
        timeout = 1000
    GLib.timeout_add(timeout, lambda *args: dlg.hide()) 
