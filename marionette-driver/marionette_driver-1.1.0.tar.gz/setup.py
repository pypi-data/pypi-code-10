# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re
from setuptools import setup, find_packages

THIS_DIR = os.path.dirname(os.path.realpath(__name__))


def read(*parts):
    with open(os.path.join(THIS_DIR, *parts)) as f:
        return f.read()


def get_version():
    return re.findall("__version__ = '([\d\.]+)'",
                      read('marionette_driver', '__init__.py'), re.M)[0]


setup(name='marionette_driver',
      version=get_version(),
      description="Marionette Driver",
      long_description='See http://marionette-driver.readthedocs.org/',
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='mozilla',
      author='Auto-tools',
      author_email='tools-marionette@lists.mozilla.org',
      url='https://wiki.mozilla.org/Auto-tools/Projects/Marionette',
      license='MPL',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=read('requirements.txt').splitlines(),
      )
