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


class Display(object):
	""" A mixin for communicating with a display attached to the device. """

	def clearDisplay(self):
		""" Set all pixels on the display to black """
		self._performCommand("display,clear", expectedResponse="SUCCESS")

	def showStringOnDisplay(self, x, y, message, size=1):
		""" Display a string on the display at position x,y

		Size must be an integer greater than or equal to one
		"""
		command = "display,showString,{},{},{},{}".format(x, y, message, size)
		self._performCommand(command, expectedResponse="SUCCESS")

	def showAristaLogoOnDisplay(self):
		""" Display the Arista logo on the display """
		self._performCommand("display,showAristaLogo", expectedResponse="SUCCESS")

	def setRotation(self, rotation):
		""" Set the screen rotation
		rotation is one of FLIP_X, FLIP_Y, FLIP_X_AND_Y, NORMAL
		"""
		command = "display,setRotation,{}".format(rotation)
		self._performCommand(command, expectedResponse="SUCCESS")

	def showAlignmentCross(self):
		""" Show a cross at the center of the display for alignment during installation	"""
		self._performCommand("display,showAlignmentCross", expectedResponse="SUCCESS")
