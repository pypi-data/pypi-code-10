import os
import sys

import drf_dynamic_fields

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = drf_dynamic_fields.__version__
name = drf_dynamic_fields.__title__

if sys.argv[-1] == 'publish':
    print('python setup.py sdist upload')
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.md').read()

setup(
    name=name,
    version=version,
    description="""A mixin to make Django Rest Framework serializers dynamically configurable.""",
    long_description=readme,
    author='Forrest Pruitt',
    author_email='forrest.pruitt@getbellhops.com',
    url='https://github.com/bellhops/drf_dynamic_fields_mixin',
    packages=[
        'drf_dynamic_fields',
    ],
    include_package_data=True,
    install_requires=[
        'djangorestframework'
    ],
    license="MIT",
    zip_safe=False,
    keywords='django-rest-framework-dynamic-fields',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
