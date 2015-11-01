import unittest

import configparser

from .checks import Asset, Page, Site


def read_config(config_path):
    config = configparser.ConfigParser()
    config.read_file(open(config_path, 'r'))
    return config_to_test_suite(config)


def config_to_test_suite(config):
    test_suite = unittest.TestSuite()
    site = None
    for section in config.sections():
        section_type, arg = section.split(' ', 1)
        if section_type == 'site':
            site = Site(arg, **config[section])
            test_suite.addTest(site)
        elif section_type == 'asset':
            site.addTest(Asset(site, arg, **config[section]))
        elif section_type == 'page':
            site.addTest(Page(site, arg, **config[section]))
        else:
            raise ReferenceError('Unknown section type: {}'.format(section_type))
    return test_suite


def run_test_suite(test_suite):
    unittest.TextTestRunner(verbosity=2).run(test_suite)
