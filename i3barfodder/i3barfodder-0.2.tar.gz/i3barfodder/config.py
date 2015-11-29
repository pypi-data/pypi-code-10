# Released under GPL3 terms (see LICENSE file)

import os
import logging
import re
from collections import abc
from . import validation


class ConfigParserError(SyntaxError):
    pass

class ConfigParser(abc.Mapping):
    """Parse INI-style string into immutable Mapping

    Main features over other INI parsers:

      - Settings above any sections are accessed via `None`.

      - The ability to use '+=' instead of '=' to append values to previously
        made settings.
    """

    COMMENT_CHAR = '#'

    _SPLIT_REGEX = re.compile(r'^'                 # Beginning of line
                              r'(\s*\[.*?)'        # Read the whole section ...
                              r'(?=^\s*(?:\[|$))', # ... up until new line with new section or EOL
                              flags=re.MULTILINE|re.DOTALL)

    _SECTION_REGEX = re.compile(r'^\s*\[([^\]\n]+?)\]\s*\n'
                                r'(.*)',
                                flags=re.DOTALL)

    _SETTING_REGEX = re.compile(r'^\s*(\w+)\s*(\+?=)\s?(.*?)$')

    def __init__(self, text):
        # Remove empty lines and comments
        clean_text = ''
        for line in text.split('\n'):
            stripped_line = line.strip()
            if stripped_line != '' and stripped_line[0] != self.COMMENT_CHAR:
                clean_text += line + '\n'

        sections = { None: {} }
        order = []

        # Iterate over sections
        for section_str in self._SPLIT_REGEX.split(clean_text):
            if section_str == '':
                continue

            section_match = self._SECTION_REGEX.match(section_str)
            if section_match is None:
                # Default section
                section_name = None
                settings_str = section_str
            else:
                section_name = section_match.group(1)
                settings_str = section_match.group(2)

            settings = {}
            for line in settings_str.split('\n'):
                if line == '':
                    continue
                setting_match = self._SETTING_REGEX.match(line)
                if setting_match is None:
                    if any(c in line for c in '[]'):
                        # line is probably intended be a section
                        raise ConfigParserError('Invalid section: {!r}'.format(line))
                    else:
                        msg = 'Invalid setting'
                        if section_name is not None:
                            msg += ' in section {!r}'.format(section_name)
                        msg += ': {!r}'.format(line)
                        raise ConfigParserError(msg)
                else:
                    name = setting_match.group(1)
                    op = setting_match.group(2)
                    value = setting_match.group(3)
                    if op == '=':
                        settings[name] = value
                    elif op == '+=':
                        if name not in settings:
                            settings[name] = ''
                        settings[name] += value

            sections[section_name] = settings
            if section_name is not None:
                order.append(section_name)

        self._sections = sections
        self._order = tuple(order)

    @property
    def order(self):
        return self._order

    def __getitem__(self, item):
        return self._sections[item]

    def __iter__(self):
        return iter(self._sections)

    def __len__(self):
        return len(self._sections)


class ConfigError(Exception):
    pass

class Config(abc.Mapping):
    DEFAULTS = {
        'delay': 0.1,
        'show_updates': False,
    }

    GLOBAL_ONLY_VARS = ('delay', 'show_updates', 'logfile', 'PATH')

    VALIDATORS = {
        'delay': lambda v: validation.validate_number(v, min=0),
        'show_updates': validation.validate_bool,
        'logfile': validation.validate_path,
        'PATH': validation.validate_PATH,
    }

    def __init__(self, config):
        self._cfg = validation.VDict(validators=self.VALIDATORS,
                                     **self.DEFAULTS)

        # Get raw ini string
        if isinstance(config, str):
            # If there's no newline, it's a file path
            if '\n' in config:
                ini_str = config
            else:
                try:
                    ini_str = open(config, 'r').read()
                except OSError as e:
                    raise ConfigError(e.strerror)
        elif hasattr(config, 'read') and callable(config.read):
            ini_str = config.read()
        else:
            raise ConfigError('Nonsensical config object: {!r}'.format(config))

        # Parse raw ini string into dict
        try:
            usrcfg = ConfigParser(ini_str)
        except ConfigParserError as e:
            raise ConfigError(e)

        # Override global user settings
        for var,val in usrcfg[None].items():
            try:
                self._cfg[var] = val
            except ValueError as e:
                raise ConfigError('Invalid {!r} value: {}'.format(var, e))

        # Copy sections, but not the main section (None)
        self._sections = dict((name,settings) for name,settings in usrcfg.items()
                              if name is not None)

        # The order of sections is also important
        self._order = usrcfg.order
        del usrcfg

        # Any globally set variable in the None section that is not
        # exclusively global is assumed to be a worker variable that is set
        # for all workers.
        for var in self._cfg.keys():
            if var not in self.GLOBAL_ONLY_VARS:
                val = self._cfg[var]
                for name in self._sections.keys():
                    section = self._sections[name]
                    if var not in section:
                        section[var] = val

        # For each section, set variable 'name' to the section name if not
        # specified.
        for name in self._sections.keys():
            section = self._sections[name]
            if 'name' not in section:
                section['name'] = name

    @property
    def order(self):
        return self._order

    @property
    def sections(self):
        return self._sections

    def __getitem__(self, name):
        return self._cfg[name]

    def __iter__(self):
        return iter(self._cfg)

    def __len__(self):
        return len(self._cfg)



def log_to_file(path):
    """Redirect all logging to file `path`"""
    try:
        file_handler = logging.FileHandler(filename=path, mode='w')
    except OSError as e:
        raise ConfigError(e.strerror)
    else:
        root_logger = logging.getLogger()

        # Copy formatter from original handler to file handler
        formatter = root_logger.handlers[0].formatter
        file_handler.setFormatter(formatter)

        # Start logging to file
        root_logger.addHandler(file_handler)
        logging.info('Started logging to {!r}'.format(path))

        # Stop logging to stderr
        for handler in root_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                root_logger.removeHandler(handler)
