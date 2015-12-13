import sys
import re
from setuptools import setup

if not ('2.6' <= sys.version < '3.0'):
    raise ValueError("Sorry, I'm not currently supporting any versions "
                     "less than 2.7 or version 3")

version_file = "makerbot_driver/_version.py"
line = open(version_file, "rt").read()
version_regex = r"^__version__\s*=\s*['\"]([^'\"]*)['\"]"
mo = re.search(version_regex, line, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % version_file)

setup(
    name='makerbot_driver',
    version=version,
    author=['Matt Mets', 'David Sayles (MBI)', 'Far McKon (MBI)'],
    author_email=['cibomahto@gmail.com', 'david.sayles@makerbot.com',
                  'far@makerbot.com'],
    packages=[
        'makerbot_driver',
        'makerbot_driver.EEPROM',
        'makerbot_driver.Encoder',
        'makerbot_driver.FileReader',
        'makerbot_driver.Firmware',
        'makerbot_driver.Gcode',
        'makerbot_driver.GcodeProcessors',
        'makerbot_driver.Writer'
    ],
    package_data={'makerbot_driver.EEPROM': ['*.json'],
                  'makerbot_driver.Firmware': ['*.conf']},
    url='http://github.com/makerbot/s3g',
    license='GNU AFFERO GENERAL PUBLIC LICENSE',
    description='Python driver to connect to MakerBot 3D Printers which use the s3g protocol',
    long_description=open('README.md').read(),
    platforms='any',
    install_requires=['pyserial']
)
