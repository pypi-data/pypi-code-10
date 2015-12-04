import os
del os.link
try:
    import pytest
except ImportError:
    raise SystemExit('We require pytest. Sorry! Install it and try again: https://pypi.python.org/pypi/pytest')

try:
    from setuptools import setup
    from setuptools.command.test import test as TestCommand
except ImportError:
    raise SystemExit('We require setuptools. Sorry! Install it and try again: http://pypi.python.org/pypi/setuptools')


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


# Integration with setuptools/distribute test commands
# define cmd class
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        pytest.main(self.test_args)

setup(
    name='django-view-acl',
    version='0.2',
    packages=['view_acl'],
    author='Perfectial',
    author_email='nataliia.todosiychuk@perfectial.com',
    include_package_data=True,
    license='Apache License',
    url='https://github.com/Perfectial/django-view-acl',
    description='Views ACL plugin is a Django app to provide method for automatic permissions generation based on urlpatterns in urls.py',
    long_description=README,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
)
