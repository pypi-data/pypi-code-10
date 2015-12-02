#!/usr/bin/env python

from distutils.core import setup

setup(name='PiStorms',
    version='2.92',
    description='PiStorms libraries',
    author='mindsensors.com',
    author_email='contact@mindsensors.com',
    url='http://www.mindsensors.com',
    py_modules=['PiStorms', 'mindsensors', 'PiStormsBrowser', 'PiStormsCom', 'PiStormsDriver', 'ps_messenger_check', 'scratch'],
    data_files=[('mindsensors_images', ['btns_center.png', 'btns_left.png', 'btns_right.png', 'button.png', 'dialogbg.png', 'Exclamation-mark-icon.png', 'Pane1.png']),
    ('/etc/init.d', ['PiStormsDriver.sh', 'PiStormsBrowser.sh']),
    ('/home/pi/PiStormsprograms', ['0-About_Me.py', '0-Scratch_PiStorms.py', '1-JesterControl.py', '1-SamTheEmotional.py', '2-CatchMike.py', '2-PyDog.py', '3-custom_i2c_test.py', '4-BatteryVolt.py', '7-SumoEyes.py', '7-touch_sensor.py', '8-GoButton.py', '8-HelloWorld.py', '9-Change_i2c_addr.py', '9-Explorer.py', '9-refresh.py', 'dog.jpg', 'dog.png', 'faceAwesome.png', 'faceClown.png', 'faceClown_eyeLeft.png', 'faceClown_eyeRight.png', 'faceClown_nose.png', 'faceHappy.png', 'faceScared2.png', 'Puppy_Dog_Barking.mp3', 'addresschange']),
    ('/home/pi/Documents/Scratch Projects/PiStorms',['PiStorms-EV3AmbientLight.sb', 'PiStorms-EV3Color.sb', 'PiStorms-EV3Gyro.sb', 'PiStorms-EV3IRDistance.sb', 'PiStorms-EV3IRRemote.sb', 'PiStorms-EV3TouchSensor.sb', 'PiStorms-EV3Ultrasonic.sb', 'PiStorms-JoyStick.sb', 'PiStorms-MotorDemo.sb', 'PiStorms-NXTAmbientLight.sb', 'PiStorms-NXTColor.sb', 'PiStorms-NXTTouchSensor.sb', 'PiStorms-printing.sb', 'PiStorms-ReadEncoder.sb', 'PiStorms-RemoteRobot.sb', 'PiStorms-Sumoeyes.sb', 'PiStorms-Template.sb', 'PiStorms-TouchScreen.sb', 'PiStorms-TouchSensor.sb']),
    ('/home/pi/.config/autostart',['tightvnc.desktop'])],
    install_requires=['mindsensors_i2c', 'mindsensorsUI', 'RPi.GPIO'],
    )