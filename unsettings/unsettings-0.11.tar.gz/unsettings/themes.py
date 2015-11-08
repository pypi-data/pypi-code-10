#!/usr/bin/env python
#-*- coding: utf-8-*-

import xdg, xdg.BaseDirectory, xdg.IniFile
import os, os.path, glob, logging
from gi.repository import Gtk

import dialogs

METACITY = 'metacity'
GTK = 'gtk'
ICON = 'icon'
CURSOR = 'cursor'
UNITY = 'unity'
KEY = 'key'

class Theme(object):
    def __init__(self, path):
        self.path = path
        
        self.base = os.path.basename(path)
        self.hidden = False
        self.name = self.base
        self.comment = ''
        self.contains = {}
        self.valid_for=set()
        
        self._check_theme()

    def _check_theme(self):
        self._check_subdirs()
        self._check_gtk3_theme()
        self._check_index_theme()
        logging.debug('"%s" contains: %s' % (self.name, self.contains))
                      


    def _check_subdirs(self):
        dirs = {
            'metacity-1': METACITY,
            #'gtk-2.0': GTK,
            'unity': UNITY,
            'gtk-2.0-key': KEY,
            'cursors': CURSOR,            
            }
        for k,v in dirs.iteritems():
            dir = os.path.join(self.path, k)
            if os.path.isdir(dir):
                self.contains[v] = None

    def _check_gtk3_theme(self):
        dir = os.path.join(self.path, 'gtk-3.0')
        if not os.path.isdir(dir):
            return
        
        if os.path.isfile(os.path.join(dir, 'gtk-keys.css')):
            self.contains[KEY] = None
        
        _name = os.path.join(dir, 'gtk-keys.css')
        if glob.glob(os.path.join(dir, '*')) != [_name]:
            self.contains[GTK] = None

    def _check_index_theme(self):
        fname =  os.path.join(self.path, 'index.theme')
        if not os.path.isfile(fname):
            return
        try:
            parser =  xdg.IniFile.IniFile(fname)
        except xdg.Exceptions.ParsingError, e:
            dialogs.error(unicode(e))
            return
        self._check_gnome_meta_theme(parser)
        self._check_desktop_entry(parser)
        self._check_icon_theme(parser)

    def _check_gnome_meta_theme(self, parser):
        group = 'X-GNOME-Metatheme'
        if not parser.hasGroup(group):
            return
        
        if parser.hasKey('Name', group):
            self.name = parser.get('Name', group, True).encode('utf-8')

        if parser.hasKey('Comment', group):
            self.comment = parser.get('Comment', group, True).encode('utf-8')
            
        if parser.hasKey('Hidden', group):   
            self.hidden = True
            
        if parser.hasKey('MetacityTheme', group):
            t = parser.get('MetacityTheme', group)
            if t != self.base:                
                self.contains[METACITY] = t

        if parser.hasKey('GtkTheme', group):
            t = parser.get('GtkTheme', group)
            if t != self.base:                
                self.contains[GTK] = t

        if parser.hasKey('IconTheme', group):
            t = parser.get('IconTheme', group)
            if t != self.base:                
                self.contains[ICON] = t

        if parser.hasKey('CursorTheme', group):
            t = parser.get('CursorTheme', group)
            if t != self.base:                
                self.contains[CURSOR] = t

    def _check_desktop_entry(self, parser):
        group = 'Desktop Entry'
        if not parser.hasGroup(group):
            return

        if parser.hasKey('Name', group):
            self.name = parser.get('Name', group, True).encode('utf-8')

        if parser.hasKey('Comment', group):
            self.comment = parser.get('Comment', group, True).encode('utf-8')
            
        if parser.hasKey('Hidden', group):   
            self.hidden = True

    def _check_icon_theme(self, parser):
        group = 'Icon Theme'
        if not parser.hasGroup(group):
            return

        if parser.hasKey('Name', group):
            self.name = parser.get('Name', group, True).encode('utf-8')

        if parser.hasKey('Comment', group):
            self.comment = parser.get('Comment', group, True).encode('utf-8')
        
        if parser.hasKey('Directories', group):
            self.contains[ICON] = None

        if parser.hasKey('Hidden', group):   
            self.hidden = True

        # print '_CHECK ICON:',  self.contains, self.path

    def verify(self, themes):
        if not self.hidden:
            for k in (METACITY, GTK, ICON, CURSOR, UNITY, KEY):
                if self._verify_type(k, themes):
                    self.valid_for.add(k)


    def _verify_type(self, type, all_themes):
        if type in self.contains:
            if self.contains[type] is None: 
                return True
            else:
                parent = self.contains[type]
                if parent in all_themes:
                    return all_themes[parent]._verify_type(type, all_themes)
                else:
                    return False
        else:
            return False


    def is_valid_for(self, type):
        return type in self.valid_for
        


def _get_theme_base_dirs():
    result = []
    for base in ('.themes', '.icons'):
        dir = os.path.expanduser('~/%s' % base)
        if os.path.isdir(dir):
            result.append(dir)
    for base in xdg.BaseDirectory.xdg_data_dirs:
        for name in ('cursors', 'icons', 'themes'):
            dir = os.path.join(base, name)
            if os.path.isdir(dir):
                result.append(dir)
    return result

def get_all_themes():
    all = {}
    result=[]

    for base in _get_theme_base_dirs():
        if os.path.isdir(base):
            for _dir in os.listdir(base):
                dir = os.path.join(base, _dir)
                if os.path.isdir(dir) and not os.path.islink(dir):
                    theme = Theme(dir)
                    all[_dir] = theme

    for theme in all.values():
        theme.verify(all)
        result.append(theme)

    return result


            
def create_theme_view(cbox):
    model = Gtk.ListStore(str, str, str)
    model.set_sort_column_id(0, Gtk.SortType.ASCENDING)
    
    cell = Gtk.CellRendererText()
    cell.set_property("max-width-chars", 30)
    cell.set_property("ellipsize", True)
    cbox.pack_start(cell, True)
    cbox.add_attribute(cell, 'text', 0)

    cell = Gtk.CellRendererText()
    cell.set_property("max-width-chars", 50)
    cell.set_property("ellipsize", True)


    cbox.pack_end(cell, True)
    cbox.add_attribute(cell, 'text', 1)

    cbox.set_id_column(2)
    cbox.set_model(model)
    

def load_themes(tv_gtk, tv_metacity, tv_icons, tv_cursor):
    themes =  get_all_themes()
    
    lists = (
        {'tv': tv_icons, 'model': tv_icons.get_model(), 
         'key': ICON
         },
        {'tv': tv_metacity, 'model': tv_metacity.get_model(), 
         'key': METACITY
         },
        {'tv': tv_cursor, 'model': tv_cursor.get_model(), 
         'key': CURSOR
         },
        {'tv': tv_gtk, 'model': tv_gtk.get_model(), 
         'key': GTK
         },
        )
    for l in lists:
        l['active'] = l['tv'].get_active_id()
        l['model'].clear()

    for theme in themes:
        for l in lists:
            if theme.is_valid_for(l['key']):
                l['model'].append([theme.name, theme.comment, theme.base])

    for l in lists:
        l['tv'].set_model(l['model'])
        l['tv'].set_active_id(l['active'])



if __name__ == '__main__':
    print 'BASE:', _get_theme_base_dirs()
    for theme in get_all_themes():
        print 'THEME %s'% theme.name
        print '   comment: %s'% theme.comment
        print '   contains: %s'% theme.contains   
        print '   path: %s'%theme.path
