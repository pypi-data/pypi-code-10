try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Python client API for the pk port knocking server daemon',
    'author': 'Anson Rosenthal',
    'url': 'https://github.com/anrosent/pk-client-python',
    'author_email': 'anson.rosenthal@gmail.com',
    'version': '0.2',
    'install_requires': ['nose'],
    'packages': ['pk_client'],
    'scripts': [],
    'name': 'pk-client-python'
}

setup(**config)
