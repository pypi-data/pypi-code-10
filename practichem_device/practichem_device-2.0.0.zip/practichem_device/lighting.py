"""
Copyright 2015 Practichem, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class Lighting(object):
	""" A mixin class for controlling lighting attached to a device """

	def __init__(self):
		super().__init__()

	def turnOnAllLedsWithFadingInMilliseconds(self, color, fadeRateInMilliseconds):
		""" Fade on all of the LEDs to a specific color.
		:param color: A Color object with RGB
		:param fadeRateInMilliseconds: Time to complete the fade in milliseconds
		"""
		command = "lightingBoard,setAllLeds,FADE_UP,{},{},{},{}".format(fadeRateInMilliseconds, color.getRed(), color.getGreen(), color.getBlue())
		self._performCommand(command, expectedResponse="SUCCESS")

	def turnOffAllLedsWithFadingInMilliseconds(self, fadeRateInMilliseconds):
		""" Fade off all of the LEDs
		:param fadeRateInMilliseconds: Time to complete the fade in milliseconds
		"""
		command = "lightingBoard,setAllLeds,FADE_DOWN,{}".format(fadeRateInMilliseconds)
		self._performCommand(command, expectedResponse="SUCCESS")

	def pulseAllLedsWithFadingInMilliseconds(self, color, fadeRateInMilliseconds):
		""" Continuously fade all of the LEDs from the color to black
		:param color: A Color object
		:param fadeRateInMilliseconds: Time to complete a full fade cycle
		"""
		command = "lightingBoard,setAllLeds,FADE_UP_THEN_DOWN,{},{},{},{}".format(fadeRateInMilliseconds, color.getRed(), color.getGreen(),
																				  color.getBlue())
		self._performCommand(command, expectedResponse="SUCCESS")

	def turnOnAllLeds(self, color):
		""" Set all of the LEDs to a color
		:param color: A Color object
		"""
		command = "lightingBoard,setAllLeds,FADE_OFF,{},{},{}".format(color.getRed(), color.getGreen(), color.getBlue())
		self._performCommand(command, expectedResponse="SUCCESS")

	def turnOnSingleLedWithFadingInMilliseconds(self, ledPosition, color, fadeRateInMilliseconds):
		""" Fade in a single LED to the chosen color.
		:param ledPosition: Zero based index of the LED to fade
		:param color: A Color object
		:param fadeRateInMilliseconds: Time to complete the fade in milliseconds
		"""
		command = "lightingBoard,setSingleLed,FADE_UP,{},{},{},{},{}".format(ledPosition, fadeRateInMilliseconds, color.getRed(), color.getGreen(),
																			 color.getBlue())
		self._performCommand(command, expectedResponse="SUCCESS")

	def turnOffSingleLedWithFadingInMilliseconds(self, ledPosition, fadeRateInMilliseconds):
		""" Fade out a single LED to off.
		:param ledPosition: Zero based index of the LED to fade
		:param fadeRateInMilliseconds: Time to complete the fade in milliseconds
		"""
		command = "lightingBoard,setSingleLed,FADE_DOWN,{},{}".format(ledPosition, fadeRateInMilliseconds)
		self._performCommand(command, expectedResponse="SUCCESS")

	def turnOnSingleLed(self, ledPosition, color):
		""" Set the color of one LED.
		:param ledPosition: Zero based index of the LED to set
		:param color: A Color object
		"""
		command = "lightingBoard,setSingleLed,FADE_OFF,{},{},{},{}".format(ledPosition, color.getRed(), color.getGreen(), color.getBlue())
		self._performCommand(command, expectedResponse="SUCCESS")

	def pulseSingleLedWithFadingInMilliseconds(self, ledPosition, color, fadeRateInMilliseconds):
		""" Continuously fade in and out a single LED.
		:param ledPosition: Zero based index of the LED to set
		:param color: A Color object
		:param fadeRateInMilliseconds: Time to complete a full fade cycle
		"""
		command = "lightingBoard,setSingleLed,FADE_UP_THEN_DOWN,{},{},{},{},{}".format(ledPosition, fadeRateInMilliseconds, color.getRed(),
																					   color.getGreen(), color.getBlue())
		self._performCommand(command, expectedResponse="SUCCESS")

	def turnOffAllLeds(self):
		""" Set all LEDs to off. """
		command = "lightingBoard,setAllLeds,FADE_OFF,0,0,0"
		self._performCommand(command, expectedResponse="SUCCESS")