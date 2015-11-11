# coding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'six',
    'Django>=1.4',
    'requests>=1.0',
]

test_requirements = [
    'tox'
]

setup(
    name="django-briteverify",
    version='1.0',

    author="Uploadcare LLC",
    author_email="hello@uploadcare.com",
    url="https://github.com/uploadcare/django-briteverify",

    description=("Integration with briteverify API"),
    long_description=readme,

    packages=[
        'django_briteverify',
    ],
    package_dir={'django_briteverify':
                 'django_briteverify'},
    install_requires=requirements,
    license="MIT",
    keywords='django briteverify',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
