from distutils.core import setup
from holding_page import __version__

version = __version__
setup(
    name='django-holding-page',
    version=version,
    packages=['holding_page', 'holding_page.subscribers', 'holding_page.subscribers.migrations'],
    url='https://github.com/danux/django-holding-page/',
    license='MIT',
    author='Daniel Davies',
    author_email='danieldavies127@gmail.com',
    description='A viral holding page to collect email address with export and unsubscribe functionality.'
)
