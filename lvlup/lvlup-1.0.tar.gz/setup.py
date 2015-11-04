""" An audio module to play audio files directly
in the command line using afplay.
"""

from setuptools import setup

setup(
    name='lvlup',
    version='1.0',
    description='Leveling up from the command line',
    url='http://github.com/keithalpichi/lvlup',
    author='Keith Alpichi',
    author_email='info@keithalpichi.com',
    license='MIT',
    packages=['lvlup'],
    keywords='afplay audio sound play music',

    # Module requires the use of afplay
    # (install using "pip install afplay")
    install_requires=['afplay']
)
