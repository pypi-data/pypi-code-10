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

from gi.repository import Gtk
import os, os.path, time, shutil, sys, logging, argparse
import gettext, locale
from gettext import gettext as _
import i18n, connection, backends, widgets, ui, settings, clipboard, optionfile, dialogs, themes, about, statusbar, zgutils, messages



class Unsettings(object):
    def __init__(self, file=None):
        
        if not settings.UNITY_MAJOR_VERSION in [5,7]:
            msg = "Sorry, %s doesn't work with your version of Unity (%s)." % (
                settings.APP_NAME,
                setting.UNITY_VERSION 
                )
            dialogs.error(msg)
            sys.exit(1)

        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(settings.GETTEXT_DOMAIN)
        self.builder.add_from_file(os.path.join(settings.UI_DIR, 
                                                'unsettings.ui'))
        self.builder.connect_signals(self)
        
        about.add_help_menu(self.obj('menu_help'))
        self.win = self.obj('window1')
        _statusbar = self.obj('statusbar')
        _statusbar.push(_statusbar.get_context_id('default'),
                        _('Click the "Apply" button to apply your settings.'))
        statusbar.init(self.obj('statusbar'))

        self.clip = clipboard.ContainerClipboard(self.obj('box_main'))
        self.clip.add_actions(cut=self.obj('ac_cut'),
                              copy=self.obj('ac_copy'),
                              paste=self.obj('ac_paste'),
                              delete=self.obj('ac_delete'))

        self.win.show()

        self.factory = widgets.WidgetFactory(self.builder)
        self.gsettings = backends.CombinedDict()      


        self.init_theme_lists()

        self.connections = connection.ConnectionGroup(self.gsettings)

        self.needs_login = connection.ConnectionGroup(self.gsettings)

        self.hide_disabled_widgets()
        self.hide_disabled_sections()     
        self.optionfile = optionfile.OptionFile(self.gsettings, 
                                                self.connections,
                                                self.win)
       

        if file is not None:
            self.optionfile.load_file(file)
        self.connections.view()
                           

                
    def hide_disabled_sections(self):
        notebook = self.obj('notebook')
        disabled_pages = set()
        for section in ui.sections:
            if not section.is_enabled():
                disabled_pages.add(self.obj(section.label))
        
        to_remove = set()
        for n in range(notebook.get_n_pages()):
            page = notebook.get_nth_page(n)    
            label = notebook.get_tab_label(page)
            if label in disabled_pages:
               to_remove.add(n) 
        for n in reversed(sorted(to_remove)):
            notebook.remove_page(n) 
    

    def hide_disabled_widgets(self):
        visible_widgets = set()  # avoid to hide widgets we already have shown
        visible_labels = set()   # avoid to hide labels we already have shown
        for option in ui.options:
            widget = option.get_widget(self.factory)
            if option.is_enabled():
                uri = option.get_uri()
                if uri is not None:
                    self.connections.add(uri,
                                         widget,
                                         converter = option.get_converter(),
                                         default = option.default,
                                     )
                if option.data is not None:
                    widget.set_data(option.data)
                widget.show()
                visible_widgets.add(widget)
                visible_labels.update(option.related)
                for o in option.related:
                    self.obj(o).show()
                if option.needs_login:
                    self.needs_login.add(option.get_uri(),
                                         widget,
                                         converter = option.get_converter(),
                                         default = option.default
                                         ) 
                
            else:
                if widget not in visible_widgets:
                    widget.hide()
                    for o in option.related:
                        if o not in visible_labels:
                            self.obj(o).hide()

    
    def init_theme_lists(self):
        lists = ('cbox_themes_gtk', 'cbox_themes_metacity', 
                 'cbox_themes_icons', 'cbox_themes_cursor')
        for cbox in lists:
            themes.create_theme_view(self.obj(cbox))
        self.update_theme_lists()
       
    def update_theme_lists(self):
        themes.load_themes(self.obj('cbox_themes_gtk'),
                           self.obj('cbox_themes_metacity'),
                           self.obj('cbox_themes_icons'),
                           self.obj('cbox_themes_cursor'))
 

    def save_options(self):
        self.optionfile.save()

    def load_options(self):
        self.optionfile.load()


    def apply_settings(self):
        with statusbar.Status(_('Applying settings ...'), 
                              _('Settings applied.')) as status:
            needs_login = self.needs_login.is_dirty()            
            self.connections.store()            
            time.sleep(settings.SLEEP_TIME)

        if needs_login:
            dialogs.information(self.win, _('Information'),
                                _('Some changes take effect next time you log in.'))
    
    def about(self):
        about.show_about_dialog()
        

    def obj(self, name):
    	"""
	get object 'name' from builder
	"""
        return self.builder.get_object(name)
        
    def run(self):
    	"""
	start the GTK main loop
	"""
        try:
            Gtk.main()
        except KeyboardInterrupt:
            Gtk.main_quit()
    
    def quit(self):
    	"""
	quit the GTK main loop
	"""
        if self.connections.is_dirty():
            answer = dialogs.yes_no_cancel_question(self.win,
                                                    _('Apply settings now?'),
                                                    _('You have changed some settings. Do you want to apply the settings before you quit?')
                                                    )
            if answer == Gtk.ResponseType.YES:
                self.apply_settings()
            elif answer == Gtk.ResponseType.CANCEL:
                return
        Gtk.main_quit()



#####################
## signal handlers
#####################

###############
## main window

    def on_window1_delete_event(self, *args):
        self.quit()

###############
## buttons

    def on_b_clear_gvfs_clicked(self, *args):
        def func():
            if not os.path.isdir(settings.GVFS_METADATA_PATH):
                return
            try:
                shutil.rmtree(settings.GVFS_METADATA_PATH)
            except Exception as e:
                dialogs.error(messages.clear_gvfs_meta_error_error % e)
                return True
            
        dialogs.cleaning_dlg(func, messages.clear_gvfs_meta_msg,
                              messages.clear_gvfs_meta_explanation)


    def on_b_clear_libdvdcss_clicked(self, *args):
        def func():
            if not os.path.isdir(settings.LIBDVDCSS_KEYS_PATH):
                return
            try:
                shutil.rmtree(settings.LIBDVDCSS_KEYS_PATH)
            except Exception as e:
                dialogs.error(messages.clear_dvdcss_keys_error % e)
                return True
            
        dialogs.cleaning_dlg(func, messages.clear_dvdcss_keys_msg,
                             messages.clear_dvdcss_keys_explanation)

    def on_b_clear_thumbnails_clicked(self, *args):
        def func():
            if not os.path.isdir(settings.THUMBS_CACHE_PATH):
                return
            try:
                shutil.rmtree(settings.THUMBS_CACHE_PATH)
                os.makedirs(settings.THUMBS_CACHE_PATH)
            except Exception as e:
                dialogs.error(messages.clear_thumbs_cache_error % e)
                return True
            
        dialogs.cleaning_dlg(func, messages.clear_thumbs_cache_msg,
                             messages.clear_thumbs_cache_explanation)

    def on_b_clear_zeitgeist_clicked(self, *args):
        def func():
             zgutils.zeitgeist_clear_all()
        dialogs.cleaning_dlg(func, messages.clear_zeitgeist_msg,
                             messages.clear_zeitgeist_explanation)

    def on_b_clear_recent_files_clicked(self, *args):
        def func():
            rman = Gtk.RecentManager.get_default()
            rman.purge_items()
        dialogs.cleaning_dlg(func, messages.clear_recent_activate_msg,
                             messages.clear_recent_activate_explanation)
        


    def on_b_userdir_clicked(self, widget, *args):
        dirs = ('desktop', 'download', 'templates',
                'public', 'documents', 'music', 'pictures', 'videos')


        path = dialogs.ask_for_file_name(
            title=_('Select folder'),
            parent=self.win,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            )
        if path is None:
            return
        
        mapping = {}
        for d in dirs:
            button = self.obj('b_userdir_%s'%d)
            entry = self.obj('e_userdir_%s'%d)
            mapping[button] = entry

        entry = mapping.get(widget)
        entry.set_text(path)
        
        


###############
## actions

    def on_ac_quit_activate(self, action, *args):
        self.quit()

    def on_ac_apply_activate(self, action, *args):
        self.apply_settings()
 

    def on_ac_reload_activate(self, action, *args):
        with statusbar.Status(_('Loading currently used settings ...'), 
                              _('Currently used settings loaded.')) as status:
            self.connections.view()
            time.sleep(settings.SLEEP_TIME)
     
    def on_ac_load_activate(self, action, *args):
        self.load_options()

    def on_ac_save_activate(self, action, *args):
        self.save_options()

    def on_ac_themes_reload_activate(self, action, *args):
        with statusbar.Status(_('Searching themes ...'), 
                              _('Themes loaded.')) as status:
            self.update_theme_lists()        
            time.sleep(settings.SLEEP_TIME)
            
    def on_ac_set_defaults_activate(self, action, *args):
        if not dialogs.confirmation(
                self.win, 
                _('Do you really want to set all settings to their default values?')):
            return

        with statusbar.Status(_('Loading default values ...'), 
                              _('Default values loaded.')) as status:
            self.connections.set_defaults()
            time.sleep(settings.SLEEP_TIME)

    def on_ac_about_activate(self, action, *args):
        self.about()

def parse_args():
    parser = argparse.ArgumentParser(version="%s %s"%(
        settings.APP_NAME, 
        settings.APP_VERSION)) 
    parser.add_argument('--debug', action='store_true', default=False)
    options, args = parser.parse_known_args()
    return options, args


def main():
    options, args = parse_args()
    
    log_format='%(levelname)s %(filename)s:%(funcName)s::%(message)s'
    if options.debug:
        log_file='%s.log' % settings.app_name
        try:
            os.remove(log_file)
        except:
            pass
        try:
            logging.basicConfig(level=logging.DEBUG,
                                filename=log_file,
                                format=log_format,
                            )
        except IOError as e:
            print "Error creating log file:", e
    else:
        logging.basicConfig(format=log_format)
        

    if len(args) == 0:
        args.append(None)
    if args[0] == '%f':
        args[0] = None

    app = Unsettings(args[0])
    app.run()   

if __name__ == '__main__':
    main()

