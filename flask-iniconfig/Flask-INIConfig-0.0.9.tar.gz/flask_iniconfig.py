#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import codecs
import sys

if sys.version_info < (3,):
    from ConfigParser import SafeConfigParser
    from ConfigParser import _default_dict
else:
    # pylint: disable=F0401
    from configparser import ConfigParser as SafeConfigParser
    from configparser import _default_dict


class INIConfig(SafeConfigParser):

    def __init__(self, app=None, defaults=None, dict_type=_default_dict,
                 allow_no_value=False):
        SafeConfigParser.__init__(self, defaults=defaults,
                                  dict_type=dict_type,
                                  allow_no_value=allow_no_value)
        # so the the normalization to lower case does not happen
        self.optionxform = str
        if app is not None:
            self.init_app(app)

    def _read_file(self, path, encoding=None):
        # see: https://bitbucket.org/wampeter/flask-iniconfig/issues/2
        if sys.version_info < (3,):
            assert isinstance(path, str) or isinstance(path, unicode), \
                'Invalid path type: %s' % type(path)
            self.read([path])
        else:
            assert isinstance(path, str) or isinstance(path, bytes), \
                'Invalid path type: %s' % type(path)
            if sys.version_info < (3,):
                with codecs.open(path, 'r', encoding=encoding) as fp:
                    self.readfp(fp)
            else:
                self.read([path], encoding=encoding)  # pylint: disable=E1123

    def init_app(self, app):
        self.app_config = app.config
        self.app_config.from_inifile = self.from_inifile
        self.app_config.from_inifile_sections = self.from_inifile_sections

    def from_inifile(self, path, encoding=None, objectify=False):
        self._read_file(path, encoding=encoding)
        for section in self.sections():
            options = self.options(section)
            for option in options:
                parsed_value = self.parse_value(section, option)
                if section == 'flask':
                    # flask likes its vars uppercase
                    self.app_config[option.upper()] = parsed_value
                else:
                    if objectify:
                        if not hasattr(self.app_config, section):
                            setattr(self.app_config, section, {})
                        getattr(self.app_config, section)[option] = \
                            parsed_value
                    else:
                        self.app_config.setdefault(
                            section, {})[option] = parsed_value

    def from_inifile_sections(self, path, section_list, preserve_case=False,
                              encoding=None):
        section_list.append('flask')
        section_list = set(section_list)
        self._read_file(path, encoding=encoding)
        for section in self.sections():
            options = self.options(section)
            for option in options:
                parsed_value = self.parse_value(section, option)
                if section in section_list:
                    if section == 'flask':
                        # flask likes its vars uppercase
                        self.app_config[option.upper()] = parsed_value
                    else:
                        if not preserve_case:
                            option = option.upper()
                        self.app_config[option] = parsed_value

    def parse_value(self, section, option):
        # XXX: deviates from SafeConfigParser: 1|0 evaluate to int
        for method in [self.getint, self.getfloat, self.getboolean]:
            try:
                return method(section, option)
            except ValueError:
                pass

        value = self.get(section, option).strip()
        try:
            # maybe its a dict, list or tuple
            if value and value[0] in ['[', '{', '(']:
                return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            pass

        return value
