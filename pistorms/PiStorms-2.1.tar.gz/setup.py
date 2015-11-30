#!/usr/bin/env python

from distutils.core import setup

setup(name='PiStorms',
    version='2.1',
    description='PiStorms libraries',
    author='mindsensors.com',
    author_email='contact@mindsensors.com',
    url='http://www.mindsensors.com',
    py_modules=['PiStorms', 'mindsensors', 'PiStormsBrowser', 'PiStormsCom', 'PiStormsDriver', 'ps_messenger_check'],
    data_files=[('mindsensors_images', ['btns_center.png', 'btns_left.png', 'btns_right.png', 'button.png', 'dialogbg.png', 'Exclamation-mark-icon.png', 'Pane1.png']),
    ('/etc/init.d', ['PiStormsDriver.sh', 'PiStormsBrowser.sh']),
    ('/home/pi/PiStormsprograms', ['0-About_Me.py'])],
    install_requires=['mindsensors_i2c', 'mindsensorsUI', 'RPi.GPIO'],
    )