import os
from setuptools import setup

import versioneer

VERSION = '1.2.0'

setup(
    name         = "explorers",
    version      = VERSION,
    cmdclass     = versioneer.get_cmdclass(),
    author       = "Fabien Benureau",
    author_email = "fabien.benureau@gmail.com",
    description  = 'Framework for autonomous exploration algorithms in sensorimotor spaces',
    license      = "Open Science License (see fabien.benureau.com/openscience.html",
    keywords     = "exploration learning algorithm sensorimotor robots robotics",
    download_url = 'https://github.com/humm/explorers/tarball/{}'.format(VERSION),
    url          = "github.com/humm/explorers.git",
    packages=['explorers',
              'explorers.algorithms',
              'explorers.algorithms.reuse',
              'explorers.algorithms.im',
             ],
    install_requires=['numpy', 'scicfg', 'learners', 'shapely', 'environments'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Science/Research',
    ]
)
