# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

REQUIREMENTS = 'requirements.txt'


# Taken from @SpotlightKid
# https://gist.github.com/SpotlightKid/486c711a3c14c70edb1a
def parse_requirements(requirements, ignore=('setuptools',)):
    """Read dependencies from file and strip off version numbers."""
    with open(requirements) as f:
        packages = set()
        for line in f:
            line = line.strip()
            if line.startswith(('#', '-r', '--')):
                continue
            if '#egg=' in line:
                pkg = line.split('#egg=')[1]
            else:
                pkg = line.split('==')[0]
            if pkg not in ignore:
                packages.add(pkg)
        return packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


def get_dependencies(requirements):
    """Return project dependencies as read from the requirements file"""
    r = parse_requirements(requirements)
    return [str(d.req) for d in r]


setup(
    name='django-tailordev-cms',
    version=__import__('td_cms').__version__,
    author='Julien Maupetit',
    author_email='julien@tailordev.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://bitbucket.org/tailordev/django-tailordev-cms',
    license='MIT',
    description=u' '.join(__import__('td_cms').__doc__.splitlines()).strip(),
    long_description=read_file('README.md'),
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    install_requires=get_dependencies(REQUIREMENTS),
    test_suite="runtests.runtests",
    zip_safe=False,
)
