try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Shared lib for Python server and client API for port knocking server "pk"',
    'author': 'Anson Rosenthal',
    'url': 'https://github.com/anrosent/pk-common',
    'author_email': 'anson.rosenthal@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['pk_common'],
    'scripts': [],
    'name': 'pk-common'
}

setup(**config)
