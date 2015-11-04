import unittest

import configparser

from .checks import Asset, Page, Site
from .exceptions import BadConfigException


def build_test_suite_from_file(config_file, profile=None):
    config = read_config(config_file)
    return config_to_test_suite(config, profile)


def read_config(config_file):
    config = configparser.ConfigParser()
    config.read_file(config_file)
    return config


def validate_config(config):
    """
    Check that a configs basic structure is correct - sites before assets and
    pages, for example
    """
    known_section_types = {'site', 'asset', 'page'}

    for section in config.sections():
        try:
            section_type, arg = section.split(' ', 1)
        except ValueError:
            raise BadConfigException('Bad section declaration: {}'.format(section))
        if section_type not in known_section_types:
            raise BadConfigException('Unknown section type: {}'.format(section_type))


def config_to_test_suite(config, profile=None):
    validate_config(config)

    for section in config.sections():
        section_type, arg = section.split(' ', 1)
        if section_type == 'site':
            if profile is None:
                site = Site(arg, **config[section])
                break
            elif arg == profile:
                site = Site(arg, **config[section])
                break
    else:
        if profile is None:
            raise BadConfigException('No sites defined in config')
        else:
            raise BadConfigException('Site profile {} not found'.format(profile))

    for section in config.sections():
        section_type, arg = section.split(' ', 1)
        if section_type == 'site':
            pass
        elif section_type == 'asset':
            site.addTest(Asset(site, arg, config[section]))
        elif section_type == 'page':
            site.addTest(Page(site, arg, config[section]))

    test_suite = unittest.TestSuite()
    test_suite.addTest(site)
    return test_suite


def run_test_suite(test_suite):
    unittest.TextTestRunner(verbosity=2).run(test_suite)
