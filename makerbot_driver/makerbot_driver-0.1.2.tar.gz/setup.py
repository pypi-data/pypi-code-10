# setup.py for pySerial
#
# Windows installer:
#   "python setup.py bdist_wininst"
#
# Direct install (all systems):
#   "python setup.py install"
#
# For Python 3.x use the corresponding Python executable,
# e.g. "python3 setup.py ..."
import sys
from setuptools import setup

if '2.6' <= sys.version < '3.0':
    import makerbot_driver

    version = makerbot_driver.__version__
else:
    raise ValueError("Sorry, I'm not currently supporting any versions "
                     "less than 2.7 or version 3")

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
    requires=['unittest2', 'pyserial', 'Mock']
)
