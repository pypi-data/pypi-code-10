from setuptools import setup

import cpplint_junit


def get_long_description():
    with open('README.rst') as file:
        description = file.read()
    return description


setup(
    name='cpplint-junit',
    version=cpplint_junit.__version__,

    description='Converts cpplint output to JUnit format.',
    long_description=get_long_description(),
    keywords='cpplint C++ Google JUnit',

    author='John Hagen',
    author_email='johnthagen@gmail.com',
    url='https://github.com/johnthagen/cpplint-junit',
    license='MIT',

    py_modules=['cpplint_junit'],
    zip_safe=False,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],

    scripts=['cpplint_junit.py']
)
