try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Runner Variant of Netcat',
    'author': 'Mark Ramach',
    'url': 'https://github.com/CenturylinkTechnology/wf-pycat.git',
    'download_url': 'https://github.com/CenturylinkTechnology/wf-pycat',
    'author_email': 'mark.ramach@centurylink.com',
    'version': '0.0.1',
    'install_requires': ['requests>=2.7',
                         'pycrypto',
                         'consulate',
                         'sh',
                         'argparse'],
    'package_dir': {'':'lib'},
    'packages': ['pycat'],
    'scripts': [],
    'name': 'wf-pycat'
}

setup(**config)
