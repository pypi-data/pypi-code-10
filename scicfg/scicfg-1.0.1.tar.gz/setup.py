from setuptools import setup

import versioneer

VERSION = '1.0.1'

setup(name         = 'scicfg',
      version      = VERSION,
      cmdclass     = versioneer.get_cmdclass(),
      author       = 'Fabien Benureau',
      author_email = 'fabien.benureau+scicfg@gmail.com',
      url          = 'https://github.com/humm/scicfg',
      download_url = 'https://github.com/humm/scicfg/tarball/{}'.format(VERSION),
      maintainer   = 'Fabien Benureau',
      license      = 'LGPLv3',
      packages     = ['scicfg'],
      description  = 'A python hierarchical configuration structure for scientific parameter files',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
      ]
     )
