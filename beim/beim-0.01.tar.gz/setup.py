#!/usr/bin/env python

name = "beim"
version = "0.01"
identifier = '%s-%s' % (name, version)


# directory structure
import os


downloadsite = 'http://dev.danse.us/packages'

console_scripts = []
gui_scripts = []
deps = []
keywords = []
url = []

def main():
    from setuptools import setup, find_packages
    setup(
        name = name,
        version = version,
        install_requires = deps,
        packages = find_packages(),
        entry_points = {
            'console_scripts': console_scripts,
            'gui_scripts': gui_scripts,
            },
        include_package_data = True,
        dependency_links = [],

        author = 'Jiao Lin',
        author_email = "linjiao@caltech.edu",
        maintainer = 'Jiao Lin',
        maintainer_email = 'linjiao@caltech.edu',
        description = 'beim: a release builder',
        # long_description = open('DESCRIPTION').read(),
        # license = open('LICENSE').read(),
        keywords = keywords,
        url = url,
        download_url = '%s/%s.tar.gz' % (downloadsite, identifier),
        # platform = ['linux', 'Mac OS X', 'Microsoft Windows'],
        )


if __name__ == '__main__': main()

