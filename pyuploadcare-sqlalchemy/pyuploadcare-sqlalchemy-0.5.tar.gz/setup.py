# coding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'six',
    'SQLAlchemy>=0.7',
    'pyuploadcare>=1',
]

test_requirements = [
    'tox'
]

setup(
    name="pyuploadcare-sqlalchemy",
    version='0.5',

    author="Uploadcare LLC",
    author_email="hello@uploadcare.com",
    url="https://github.com/uploadcare/pyuploadcare-sqlalchemy",

    description=("Custom fields types for SqlAlchemy which integrated "
                 "with Uploadcare service."),
    long_description=readme,

    packages=[
        'pyuploadcare_sqlalchemy',
    ],
    package_dir={'pyuploadcare_sqlalchemy':
                 'pyuploadcare_sqlalchemy'},
    install_requires=requirements,
    license="MIT",
    keywords='pyuploadcare sqlalchemy',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
