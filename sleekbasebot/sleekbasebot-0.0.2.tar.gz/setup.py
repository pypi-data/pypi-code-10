from setuptools import setup

setup(
  name = 'sleekbasebot',
  #package_dir = {'': 'sleekbasebot'},
  packages = ['sleekbasebot', 'sleekbasebot.commands', 'sleekbasebot.muc_logging'],
  version = '0.0.2',
  description = 'basic sleekxmpp bot with argument parsing and muc logging',
  install_requires=[
        "sleekxmpp",
    ],
  author = 'Jan Hartmann',
  author_email = 'stuff@kwoh.de',
  license='MIT',
  url = 'https://github.com/puhoy/sleekbasebot',
  keywords = ['xmpp', 'sleekxmpp', 'bot'],
  classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',

    "Operating System :: OS Independent"
],
)