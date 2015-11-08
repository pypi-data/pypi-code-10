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


from gi.repository import Gtk
from gettext import gettext as _

import json, time
import settings, ui, dialogs, statusbar


class OptionFile(object):
    def __init__(self, gsettings, connections, win):
        self.gsettings = gsettings
        self.connections = connections
        self.win = win


    def check_data(self, d):        
        msg=''
        if d.get('UNITY_MAJOR_VERSION', None) != settings.UNITY_MAJOR_VERSION:
            msg+=_('This file has been created with a different version of Unity.\n')
        if d.get('APP_VERSION', None) != settings.APP_VERSION:
            msg+=_('This file has been created with a different version of Unsettings.\n')
        return msg

    def add_file_chooser_filters(self, dialog):
        filter = Gtk.FileFilter()
        filter.set_name(_("Unsettings files"))
        filter.add_pattern('*%s'%settings.DUMPFILE_EXT)
        dialog.add_filter(filter)

        filter = Gtk.FileFilter()
        filter.set_name(_("Any files"))
        filter.add_pattern("*")
        dialog.add_filter(filter)

    def save(self):
        meta = {
            'FORMAT': settings.DUMPFILE_FORMAT,
            'UNITY_MAJOR_VERSION': settings.UNITY_MAJOR_VERSION,
            'UNITY_VERSION': settings.UNITY_VERSION,
            'APP': settings.APP_NAME,
            'APP_VERSION': settings.APP_VERSION
            }
        dialog = Gtk.FileChooserDialog(_("Save To File"), self.win,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL, 
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE, 
                                        Gtk.ResponseType.OK))
        self.add_file_chooser_filters(dialog)
        dialog.set_do_overwrite_confirmation(True)

        response = dialog.run()
        path = dialog.get_filename()
        dialog.destroy()

        if response != Gtk.ResponseType.OK:
            return

        if '.' not in path:
            path = '%s%s'%(path, settings.DUMPFILE_EXT)

        d = dict()
        for option in ui.options:
            if option.is_enabled():
                for conn in self.connections.connections:
                    uri = option.get_uri()
                    if conn.has_key(uri):
                        d[uri] = conn.get_widget_value()
        meta['options'] = d

        with statusbar.Status(_('Saving settings ...'), 
                              _('Settings saved.')) as status:
            try:
                with open(path, 'w') as f:
                    f.write(json.dumps(meta, indent=2).decode('utf-8'))
                time.sleep(settings.SLEEP_TIME)
            except Exception, e:
                status.set_end_msg(_('Settings not saved.'))
                dialogs.information(self.win, _('Information'),
                                    _("Can't write file %s: %s" % (path, e)))
                

        
    def load(self):
        dialog = Gtk.FileChooserDialog(_("Open File"), self.win,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, 
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, 
                                        Gtk.ResponseType.OK))
        self.add_file_chooser_filters(dialog)

        response = dialog.run()
        path = dialog.get_filename()
        dialog.destroy()
        
        if response != Gtk.ResponseType.OK:
            return

        self.load_file(path)

    def load_file(self, path):
        with statusbar.Status(_('Loading settings from %s...' % path), 
                              _('Settings from %s loaded.' % path)) as status:
            try:
                with open(path, 'r') as f:
                    d=json.load(f)

                msg = self.check_data(d)
                if msg !='':
                    dialogs.information(self.win, _('Warning'),
                                        "%s\n%s" % (msg,
                                                    _("Some settings may be wrong")
                                                    ))
                if 'options' in d:
                    d = d['options']
                else:
                    dialogs.information(self.win, _('Error'),
                                        _("This file doesn't contain any valid data")
                                        )
                    return False

                for option in ui.options:
                    if option.is_enabled():
                        for conn in self.connections.connections:
                            uri = option.get_uri()
                            if uri in d and conn.has_key(uri):
                                conn.set_widget_value(d[uri])
                time.sleep(settings.SLEEP_TIME)
            except Exception, e:
                status.set_end_msg(_('Settings from %s not loaded' % path))
                dialogs.information(self.win, _('Information'),
                                _("Can't read file %s: %s" % (path, e)))

        return True
    
