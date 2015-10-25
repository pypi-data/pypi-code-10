# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='PolarBird',
    version='0.0.4',
    author='Lukáš Pohlreich',
    author_email='pohlreichlukas@gmail.com',
    packages=find_packages(),
    install_requires=['twitter'],
    description=(
        'Curses based Twitter app allowing to receive tweets in realtime, '
        'compose tweets and more.'
    ),
    long_description=open('./README.rst').read(),
    license='MIT license',
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console :: Curses',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
    entry_points={
        'console_scripts': [
            'polarbird = polarbird:start_app'
        ]
    }
)
