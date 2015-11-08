
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


import i18n, converter, settings, connection
import os, os.path
from gettext import gettext as _



class Option(object):
    def __init__(self, uri, widget, 
                 min_version=None, max_version=None, related=None,
                 converter=None, needs_login=False, 
                 needs_app_restart=False, 
                 default=connection.BACKEND_DEFAULT,
                 data = None
    ):
        self.uri = uri
        self.widget = widget
        if  min_version is None:
           min_version = 0
        if  max_version is None:
            max_version = 99999
        self.min_version = min_version
        self.max_version = max_version
        if related is None:
            self.related = ()
        elif isinstance(related, (list, tuple)):
            self.related = related
        else:
            self.related = (related,)
        self.converter = converter
        self.needs_login = needs_login
        self.needs_app_restart = needs_app_restart
        self.default = default
        self.data = data


    def get_uri(self):
        return self.uri

    def get_widget(self, factory):
        return factory.get(self.widget)

    def get_converter(self):
        return self.converter

    def is_enabled(self):
        if isinstance(self.min_version, int):
            self.min_version = (self.min_version, 0, 0)
        if isinstance(self.max_version, int):
            self.max_version = (self.max_version, 999, 999)
        current_version = ( settings.UNITY_MAJOR_VERSION,
                            settings.UNITY_MINOR_VERSION,
                            settings.UNITY_REVISION_NUMBER
                        )
        return self.min_version <= current_version <= self.max_version

    
class Section(object):

    def __init__(self, label, min_version=None, max_version=None, 
                 version=None):
        self.label = label

        self.min_version = 0
        self.max_version = 999
        if version is not None:
            self.min_version = self.max_version = version
        if min_version is not None:
            self.min_version = min_version            
        if max_version is not None:
            self.max_version = max_version

    def is_enabled(self):
        if isinstance(self.min_version, int):
            self.min_version = (self.min_version, 0, 0)
        if isinstance(self.max_version, int):
            self.max_version = (self.max_version, 999, 999)

        current_version = ( settings.UNITY_MAJOR_VERSION,
                            settings.UNITY_MINOR_VERSION,
                            settings.UNITY_REVISION_NUMBER
        )
       
        return self.min_version <= current_version <= self.max_version       


sections = (
    Section('l_webapps', min_version=6, max_version=(7,3,1)),
    Section('l_keyboard', min_version=7),
    )

options = (
   Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/icon_size',
          'sc_launcher_size', max_version = 5, related='l_launcher_size',
          converter = converter.IntConverter()),

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ icon-size',
          'sc_launcher_size_v6', min_version = 6,
          related='l_launcher_size_v6',
          converter = converter.IntConverter()),

   Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/launcher_opacity',
          'sc_launcher_opacity', max_version = 5),

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ launcher-opacity',
          'sc_launcher_opacity', min_version = 6),

   Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/launcher_hide_mode',
          'cbox_launcher_hide_v5',
          min_version = 5, max_version = 5), 

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ launcher-hide-mode',
          'cbox_launcher_hide_v5', min_version = 6),

   Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/reveal_trigger',
          'cbox_launcher_reveal_trigger',
          min_version = 5, max_version = 5, related='l_launcher_reveal_trigger'), 

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ reveal-trigger',
          'cbox_launcher_reveal_trigger', min_version = 6, related='l_launcher_reveal_trigger'),

   Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/autohide_animation',
          'cbox_launcher_autohide_animation', max_version = 5), 

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ autohide-animation',
          'cbox_launcher_autohide_animation', min_version = 6),

  Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/launch_animation',
          'cbox_launcher_launch_animation', max_version = 5), 

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ launch-animation',
          'cbox_launcher_launch_animation', min_version = 6),

   Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/edge_responsiveness',
          'sc_launcher_edge_responsiveness',
           min_version = 5, max_version = 5, related='l_launcher_edge_responsiveness',
           converter=converter.FloatConverter(factor=0.78, offset=0.2)
          ), 

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ edge-responsiveness',
          'sc_launcher_edge_responsiveness', min_version = 6, related='l_launcher_edge_responsiveness',
           converter=converter.FloatConverter(factor=0.78, offset=0.2)),

  Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/reveal_pressure',
          'sc_launcher_reveal_pressure',
          min_version = 5, max_version = 5, related='l_launcher_reveal_pressure',
          converter=converter.IntConverter(factor=5, offset=1)
          ), 

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ reveal-pressure',
          'sc_launcher_reveal_pressure', min_version = 6, related='l_launcher_reveal_pressure',
          converter=converter.IntConverter(factor=5, offset=1)
          ),

  Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/background_color', 
          'colbt_launcher_background_color',
           min_version = 5, max_version = 5, related='l_launcher_background_color',
           converter = converter.RemoveAlphaConverter()
          ), 

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ background-color',
          'colbt_launcher_background_color', 
          min_version = 6, related='l_launcher_background_color',
          converter = converter.RemoveAlphaConverter()),
   Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/backlight_mode',
          'cbox_launcher_backlights', max_version = 5), 

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ backlight-mode',
          'cbox_launcher_backlights', min_version = 6),

  Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/panel_opacity',
          'sc_panel_opacity', max_version = 5),

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ panel-opacity',
          'sc_panel_opacity', min_version = 6),

  Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/dash_blur_experimental',
          'cbox_dash_blur', max_version = 5),

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ dash-blur-experimental',
          'cbox_dash_blur', min_version = 6),

   Option('gsettings://com.canonical.Unity form-factor', 
          'cbox_dash_formfactor',
          converter=converter.DictConverter({0:'Automatic', 
                                             1:'Desktop', 
                                             2:'Netbook'})
          ),

   Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/urgent_animation',
          'cbox_launcher_urgent_animation', max_version = 5),

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ urgent-animation',
          'cbox_launcher_urgent_animation', min_version = 6),

   Option('gsettings://com.canonical.Unity.Panel systray-whitelist',
          'tview_panel_systray_whitelist', 
          max_version=6, related=('l_panel_systray_whitelist',
                                  'swin_panel_systray_whitelist',
                                  ),
          converter=converter.ListConverter()
          ),

   Option('gsettings://org.gnome.settings-daemon.plugins.xsettings hinting',
          'cbox_fonts_hinting',
          converter=converter.DictConverter({0:'none', 
                                             1:'slight',
                                             2:'medium',
                                             3:'full'}),
          ),
   Option('gsettings://org.gnome.settings-daemon.plugins.xsettings antialiasing',
          'cbox_fonts_antialiasing',
          converter=converter.DictConverter({0:'none', 
                                             1:'grayscale',
                                             2:'rgba'}),
          ),

    Option('gsettings://com.canonical.Unity.Interface text-scale-factor',
           'sc_fonts_scaling', related='l_fonts_scaling',
           min_version=(7,3,2),
          ),
   Option('gsettings://org.gnome.desktop.interface font-name', 
          'fontb_fonts_default_font',
          ),
   Option('gsettings://org.gnome.desktop.interface monospace-font-name',
          'fontb_fonts_monospaced_font',
          ),
   Option('gsettings://org.gnome.desktop.interface document-font-name',
          'fontb_fonts_document_font',
          ),
   Option('gsettings://org.gnome.nautilus.desktop font',
          'fontb_fonts_desktop_font',
          converter = converter.DictConverter({'Normal': ''}),
          default=''
          ), 

   Option('gconf://apps/metacity/general/titlebar_font',
          'fontb_fonts_titlebar_font',
          max_version = 5,
          default = "Ubuntu Bold 11",
          ),

   Option('gsettings://org.gnome.desktop.wm.preferences titlebar-font',
          'fontb_fonts_titlebar_font', default = "Ubuntu Bold 11",
           min_version = 5,
          ),   

   Option('gconf://apps/compiz-1/general/screen0/options/hsize',
          'spin_windows_workspaces_x',
          converter=converter.IntConverter(),
          max_version=5,
          ),

   Option('gsettings://org.compiz.core:/org/compiz/profiles/unity/plugins/core/ hsize',

          'spin_windows_workspaces_x',
          converter=converter.IntConverter(), min_version = 6),

   Option('gconf://apps/compiz-1/general/screen0/options/vsize',
          'spin_windows_workspaces_y',
          converter=converter.IntConverter(),
          max_version=5 
          ),

   Option('gsettings://org.compiz.core:/org/compiz/profiles/unity/plugins/core/ vsize',
          'spin_windows_workspaces_y',
           converter=converter.IntConverter(), min_version = 6),


  Option('gconf://apps/metacity/general/focus_mode',  
          'sw_windows_click_to_focus', max_version = 5,
          converter=converter.DictConverter({True: 'click', 
                                             False: 'sloppy'}),
          ),

   Option('gsettings://org.gnome.desktop.wm.preferences focus-mode',
          'sw_windows_click_to_focus', min_version = 6,
          converter=converter.DictConverter({True: 'click', 
                                             False: 'sloppy'}),
          ),

   Option('gconf://apps/metacity/general/auto_raise',
          'sw_windows_auto_raise', max_version=5,
          ), 

   Option('gsettings://org.gnome.desktop.wm.preferences auto-raise',
          'sw_windows_auto_raise', min_version = 6,
          ),

  Option('gconf://apps/metacity/general/auto_raise_delay',
          'sc_windows_auto_raise_delay', max_version=5,
           converter=converter.IntConverter(factor=100)
          ), 

   Option('gsettings://org.gnome.desktop.wm.preferences auto-raise-delay',
          'sc_windows_auto_raise_delay', min_version = 6,
          converter=converter.IntConverter(factor=100)
          ), 

  Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/automaximize_value',
          'sc_windows_automaximize', max_version = 5,
           converter=converter.IntConverter()
          ),

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ automaximize-value',
          'sc_windows_automaximize', min_version = 6),

 Option('gsettings://com.canonical.Unity minimize-speed-threshold',
        'cbox_windows_minimize_animation', related='l_windows_minimize_animation',
        min_version = 6,converter=converter.DictConverter({0: 100, 
                                                           1: 0}),
        ),

   Option('gsettings://org.gnome.desktop.background show-desktop-icons',
          'sw_desktop_show_icons',
          ),

   Option('gsettings://org.gnome.nautilus.desktop home-icon-visible',
          'sw_desktop_show_home',
          ),
   Option('gsettings://org.gnome.nautilus.desktop computer-icon-visible',
          'sw_desktop_show_computer',
          max_version = 5, related='l_desktop_show_computer'
          ),
   Option('gsettings://org.gnome.nautilus.desktop trash-icon-visible',
          'sw_desktop_show_trash',
          ),
   Option('gsettings://org.gnome.nautilus.desktop network-icon-visible',
          'sw_desktop_show_network',
          ),

 Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/shortcut_overlay',
          'sw_desktop_shortcut_overlay',
           min_version = 5,  max_version=5, related='l_desktop_shortcut_overlay',
          ),

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ shortcut-overlay',
          'sw_desktop_shortcut_overlay', min_version = 6, related='l_desktop_shortcut_overlay'),

  Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/alt_tab_bias_viewport',
         'sw_desktop_alt_tab_current_viewport',
          min_version = 5, max_version = 5, related='l_desktop_alt_tab_current_viewport',
          converter=converter.DictConverter({True: False, 
                                             False: True}),
          ),

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ alt-tab-bias-viewport',
          'sw_desktop_alt_tab_current_viewport', min_version = 6, related='l_desktop_alt_tab_current_viewport',
          converter=converter.DictConverter({True: False, 
                                             False: True}),),
  Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/show_hud',
          'sw_windows_show_hud',
          min_version = 5, max_version = 5, related='l_windows_show_hud',
          converter=converter.DictConverter({True: '<Alt>', 
                                             False: ''}),
          ),

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ show-hud',
          'sw_windows_show_hud', related='l_windows_show_hud', min_version = 6,
          converter=converter.DictConverter({True: '<Alt>', 
                                             False: 'Disabled'}),),

   Option('gsettings://com.canonical.Unity.ApplicationsLens display-available-apps',
          'sw_dash_apps_download',
          min_version = 5, related='l_dash_apps_download'
          ),

   Option('gsettings://com.canonical.Unity.FilesLens use-locate',
          'sw_dash_search_all_files',
          min_version = 5, related='l_dash_search_all_files'
          ),

   Option('gsettings://com.canonical.Unity.ApplicationsLens display-recent-apps',
          'sw_dash_apps_recently',
          min_version = 5, related='l_dash_apps_recently'
          ),

   Option('gsettings://com.canonical.Unity.Lenses remote-content-search',
          'sw_dash_online_results',
          min_version = 6, related='l_dash_online_results',
          converter=converter.DictConverter({True: 'all', 
                                             False: 'none'}),

          ),
   Option('env://SMART_SCOPE_SERVER',
           'e_dash_shopping_url',
           min_version = 7, related=('l_dash_shopping_url',
                                     'l_default_shopping_url'),
           needs_login=True,
           converter=converter.DictConverter(
               {'https://productsearch.ubuntu.com': None, 
                
                }),
            ),   

   Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/panel_opacity_maximized_toggle',
          'sw_panel_opacity_maximized',
          min_version = 5,  max_version=5, related='l_panel_opacity_maximized'
          ),

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ panel-opacity-maximized-toggle',
          'sw_panel_opacity_maximized', min_version = 6, related='l_panel_opacity_maximized'),


   Option('gsettings://com.canonical.indicator.session show-real-name-on-panel',
          'sw_panel_show_real_name',
          min_version=5, max_version=5, related='l_panel_show_real_name', 
          needs_login=True,
          ),
 Option('gsettings://com.canonical.indicator.session show-real-name-on-panel',
          'sw_panel_show_real_name',
          min_version=6, related='l_panel_show_real_name', 
          ),

   Option('gsettings://com.canonical.indicator.session user-show-menu',
          'sw_panel_show_user_menu',
          min_version=5, max_version=5, related='l_panel_show_user_menu', 
          needs_login=True,
          ),

   Option('gsettings://com.canonical.indicator.power icon-policy',
          'cbox_panel_battery_status',
          min_version=5, related='l_panel_battery_status', 
          converter=converter.DictConverter({0: 'present', 
                                             1: 'charge',
                                             2: 'never'}),
          ),

   Option('gsettings://com.canonical.indicator.sound visible', 
          'sw_indicators_show_sound_indicator',
          min_version=5, related='l_indicators_show_sound_indicator', 
          ),

   Option('gsettings://com.canonical.indicator.bluetooth visible',
          'sw_indicators_show_bluetooth_indicator',
          min_version=5, related='l_indicators_show_bluetooth_indicator', 
          ),

   Option('gsettings://com.canonical.indicator.sound blacklisted-media-players',
          'tview_indicators_media_players_blacklist',
           min_version=5, converter=converter.ListConverter()
          ),

  Option('gconf://apps/compiz-1/plugins/unityshell/screen0/options/overcome_pressure',
          'sc_desktop_overcome_pressure',
          min_version = 5,  max_version=5, related='l_desktop_overcome_pressure',
          converter=converter.IntConverter(factor=10)
          ),

   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ overcome-pressure',
          'sc_desktop_overcome_pressure', min_version = 6, related='l_desktop_overcome_pressure',
          converter=converter.IntConverter(factor=10)),

  Option('gconf://desktop/gnome/peripherals/mouse/cursor_theme',
          'cbox_themes_cursor', max_version = 5,
           default = 'Ambiance'
          ),
 

   Option('gsettings://org.gnome.desktop.interface cursor-theme',
          'cbox_themes_cursor',
           default = 'Ambiance'
          ),

   Option('gsettings://org.gnome.desktop.interface icon-theme',
          'cbox_themes_icons',
          ),


    Option(None, 'l_themes_gtk', max_version = 6, data=_('GTK:')),
    Option(None, 'l_themes_gtk', min_version = 7, data=_('Appearance:')),

   Option('gsettings://org.gnome.desktop.interface gtk-theme',
          'cbox_themes_gtk',
          ),

  Option('gconf://apps/metacity/general/theme',
          'cbox_themes_metacity', max_version = 5,
          default = 'Ambiance'
          ),

   Option('gsettings://org.gnome.desktop.wm.preferences theme',
          'cbox_themes_metacity', related='l_themes_metacity',
           min_version = 5, max_version = 6
          ),
   Option('env://UBUNTU_MENUPROXY',
          'sw_windows_global_menu',
          needs_login=True, 
          converter=converter.DictConverter({True: None, 
                                             False: '0',}),
          ),
     
   Option('gsettings://com.canonical.Unity integrated-menus',
          'cbox_menu_in_titlebar', related='l_menu_in_titlebar',
          converter=converter.DictConverter({0: False, 
                                             1: True}),
          min_version = 7,
      ),

   Option('env://QT_X11_NO_NATIVE_MENUBAR',
          'sw_windows_global_menu',
          needs_login=True, 
          converter=converter.DictConverter({True: None, 
                                             False: '1',}),
          ),

    Option('gsettings://com.canonical.Unity always-show-menus',
           'cbox_show_global_menu', related='l_show_global_menu',
           converter=converter.DictConverter({1: False, 
                                              0: True}),
           min_version = (7,3,2),
       ),
    
    Option('env://UNITY_LOW_GFX_MODE',
          'cbox_themes_gfx_mode', related='l_themes_gfx_mode',
          needs_login=True, min_version=6,
          converter=converter.DictConverter({0: None, 
                                             1: '1'}),
          ),

   Option('gsettings://org.gnome.desktop.interface ubuntu-overlay-scrollbars',
          'sw_windows_overlay_scrollbars',   
          needs_app_restart=True, min_version = 5, max_version=5,        
          ),

   Option('gsettings://com.canonical.desktop.interface scrollbar-mode',       
          'cbox_windows_overlay_scrollbars',
          needs_app_restart=True, min_version = 6, max_version = (7,3,1),
          converter=converter.DictConverter({0: 'normal', 
                                             1: 'overlay-auto',
                                             2: 'overlay-pointer',
                                             3: 'overlay-touch',
                                             }),
          ),
    
    Option('env://GTK_OVERLAY_SCROLLING',
          'sw_windows_overlay_scrollbars',   
           needs_login=True, min_version = (7,3,2),
           converter=converter.DictConverter({0: "0", 
                                              1: None}),
          ),

   Option('gsettings://org.gnome.desktop.interface automatic-mnemonics',
          'sw_gtk_show_mnemonics',          
          ),
   Option('gsettings://org.gnome.desktop.interface buttons-have-icons',
          'sw_gtk_buttons_have_icons',
          ),
   Option('gsettings://org.gnome.desktop.interface menus-have-icons',
          'sw_gtk_menus_have_icons',
          ),
   Option('gsettings://org.gnome.desktop.interface can-change-accels',
          'sw_gtk_can_change_accels',
          ),
   Option('gsettings://org.gnome.desktop.interface cursor-blink',
          'sw_gtk_cursor_blink',
          ),

   Option('gsettings://com.canonical.unity.webapps integration-allowed',
          'sw_webapps_enable', related='l_webapps_enable',
          needs_app_restart=True, min_version = 6, max_version=(7,3,1)
          ),

   Option('gsettings://com.canonical.unity.webapps preauthorized-domains',
          'tview_webapps_preauthorized_apps',
          min_version=6, max_version=(7,3,1),
          related='l_webapps_preauthorized_apps',
          converter=converter.ListConverter()
          ),
   Option('gsettings://com.canonical.unity.webapps allowed-domains',
          'tview_webapps_allowed_apps',
          min_version=6, max_version=(7,3,1),
          related='l_webapps_allowed_apps',
          converter=converter.ListConverter()
          ),
   Option('gsettings://com.canonical.unity.webapps dontask-domains',
          'tview_webapps_dontask_apps',
          min_version=6, max_version=(7,3,1),
          related='l_webapps_dontask_apps',
          converter=converter.ListConverter()
          ),

   Option('gsettings://com.canonical.indicator.appmenu.hud store-usage-data',
          'sw_hud_usage_data',
          min_version=5, 
          ),

   Option('gsettings://com.ubuntu.geoip geoip-url',
          'sw_geoclue', related='l_geoclue',
          converter=converter.DictConverter(
              {True: 'http://geoip.ubuntu.com/lookup',
               False: 'http://localhost:0/'}),
          min_version=7
          ),
   Option('zeitgeist://enabled',
           'sw_zeitgeist_enable',
           ),
   Option('gsettings://org.compiz.unityshell:/org/compiz/profiles/unity/plugins/unityshell/ launcher-minimize-window',
           'sw_launcher_minimize_window',
           related='l_launcher_minimize_window',
           min_version=7
       ),

   Option('xkbopt://ctrl',
          'cbox_ctrl_key_position',
          min_version = 7, related='l_ctrl_key_position',
          converter=converter.DictConverter({
               0: '---',
               1: 'nocaps',
               2: 'lctrl_meta',
               3: 'swapcaps',
               4: 'ac_ctrl',
               5: 'aa_ctrl',
               6: 'rctrl_ralt',
               7: 'menu_rctrl',
               8: 'ctrl_ralt',
           })
     ),
   Option('xkbopt://compose',
          'cbox_compose_key_position',
          min_version = 7, related='l_compose_key_position',
          converter=converter.DictConverter({
               0: '---',
               1: 'ralt',
               2: 'lwin',
               3: 'lwin-altgr',
               4: 'rwin',
               5: 'rwin-altgr',
               6: 'menu',
               7: 'menu-altgr',
               8: 'lctrl',
               9: 'lctrl-altgr',
              10: 'rctrl',
              11: 'rctrl-altgr',
              12: 'caps',
              13: 'caps-altgr',
              14: '102',
              15: '102-altgr',
              16: 'paus',
              17: 'prsc',
              18: 'sclk',
           })
      ),
   Option('xkbopt://eurosign',
          'cbox_euro_position',
          min_version = 7, related='l_euro_position',
          converter=converter.DictConverter({
               0: '---',
               1: 'e',
               2: '2',
               3: '4',
               4: '5',
           })
      ),
   Option('xkbopt://rupeesign',
          'cbox_rupee_position',
          min_version = 7, related='l_rupee_position',
          converter=converter.DictConverter({
                0: '---',
                1: '4',
                })
          ),

 Option('xkbopt://keypad',
        'cbox_numpad_layout',
        min_version = 7,related='l_numpad_layout',
        converter=converter.DictConverter({
               0: '---',
               1: 'legacy',
               2: 'oss',
               3: 'future',
               4: 'legacy_wang',
               5: 'oss_wang',
               6: 'future_wang',
               7: 'hex',
               8: 'atm',
           })
          ),

Option('xkbopt://caps',
       'cbox_capslock_behaviour',
       min_version = 7,related='l_capslock_behaviour',
       converter=converter.DictConverter({
           0: '---',
           1: 'internal',
           2: 'internal_nocancel',
           3: 'shift',
           4: 'shift_nocancel',
           5: 'capslock',
           6: 'numlock',
           7: 'swapescape',
           8: 'escape',
           9: 'backspace',
           10: 'super',
           11: 'hyper',
           12: 'shiftlock',
           13: 'none',
           14: 'ctrl_modifier'
           }),
       ),
Option('xkbopt://altwin',
       'cbox_altwin_behaviour',
       min_version = 7,related='l_altwin_behaviour',
       converter=converter.DictConverter({
           0: '---',
           1: 'menu',
           2: 'meta_alt',
           3: 'alt_win',
           4: 'ctrl_win',
           5: 'ctrl_alt_win',
           6: 'meta_win',
           7: 'left_meta_win',
           8: 'hyper_win',
           9: 'alt_super_win',
           10: 'swap_alt_win',
           }),
       ),
Option('xkbopt://shift',
       'cbox_shift_behaviour',
       min_version = 7,related='l_shift_behaviour',
       converter=converter.DictConverter({
           0: '---',
           1: 'breaks_caps',
           2: 'both_capslock',
           3: 'both_capslock_cancel',
           4: 'both_shiftlock',
           }),
       ),

Option('xkbopt://kpdl',
       'cbox_numpad_del_behaviour',
       min_version = 7,related='l_numpad_del_behaviour',
       converter=converter.DictConverter({
           0: '---',
           1: 'dot',
           2: 'comma',
           3: 'dotoss',
           4: 'dotoss_latin9',
           5: 'commaoss',
           6: 'momayyezoss',
           7: 'kposs',
           8: 'semi',
           }),
       ),

 # Doesn't work in Ubunto 15.10    
 # Option('xkbopt://grp',
 #       'cbox_switch_kbd_layout',
 #       min_version = 7,related='l_switch_kbd_layout',
 #       converter=converter.DictConverter({
 #           0: '---',
 #           1: 'switch',
 #           2: 'lswitch',
 #           3: 'lwin_switch',
 #           4: 'rwin_switch',
 #           5: 'win_switch',
 #           6: 'caps_switch',
 #           7: 'rctrl_switch',
 #           8: 'toggle',
 #           9: 'lalt_toggle',
 #           10: 'caps_toggle',
 #           11: 'shift_caps_toggle',
 #           12: 'shift_caps_switch',
 #           13: 'win_menu_switch',
 #           14: 'lctrl_rctrl_switch',
 #           15: 'alt_caps_toggle',
 #           16: 'shifts_toggle',
 #           17: 'alts_toggle',
 #           18: 'ctrls_toggle',
 #           19: 'ctrl_shift_toggle',
 #           20: 'lctrl_lshift_toggle',
 #           21: 'rctrl_rshift_toggle',
 #           22: 'ctrl_alt_toggle',
 #           23: 'alt_shift_toggle',
 #           24: 'lalt_lshift_toggle',
 #           25: 'alt_space_toggle',
 #           26: 'menu_toggle',
 #           27: 'lwin_toggle',
 #           28: 'win_space_toggle',
 #           29: 'rwin_toggle',
 #           30: 'lshift_toggle',
 #           31: 'rshift_toggle',
 #           32: 'lctrl_toggle',
 #           33: 'rctrl_toggle',
 #           34: 'sclk_toggle',
 #           35: 'lctrl_lwin_rctrl_menu',
 #           }),
 #       ),

    
Option('userdir://DESKTOP',
       'e_userdir_desktop', related=('l_userdir_desktop', 'b_userdir_desktop'),
       ),
Option('userdir://DOWNLOAD',
       'e_userdir_download', related=('l_userdir_download', 'b_userdir_download'),
       ),
Option('userdir://TEMPLATES',
       'e_userdir_templates', related=('l_userdir_templates', 'b_userdir_templates'),
       ),
Option('userdir://PUBLICSHARE',
       'e_userdir_public', related=('l_userdir_public', 'b_userdir_public'),
       ),
Option('userdir://DOCUMENTS',
       'e_userdir_documents', related=('l_userdir_documents', 'b_userdir_documents'),
       ),
Option('userdir://MUSIC',
       'e_userdir_music', related=('l_userdir_music', 'b_userdir_music'),
       ),
Option('userdir://PICTURES',
       'e_userdir_pictures', related=('l_userdir_pictures', 'b_userdir_pictures'),
       ),
Option('userdir://VIDEOS',
       'e_userdir_videos', related=('l_userdir_videos', 'b_userdir_videos'),
       ),

)    
