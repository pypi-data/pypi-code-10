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
from time import sleep
import logging

from practichem_device import PractichemSerialDevice, PractichemEmulatorDevice

logger = logging.getLogger(__name__)

# see wiki pages for valves for more information
rotaryValvePositionsInDegrees = {
	"BUFFER_SELECTOR": {"Inlet1": 0, "Inlet2": 54, "Inlet3": 90, "Inlet4": 144,
						"Inlet5": 180, "Inlet6": 234, "Inlet7": 270, "Inlet8": 324},
	"COLUMN_SELECTOR": {"Bypass": 0,
						"Column1": 36, "Column2": 72, "Column3": 108, "Column4": 144,
						"Column1Reverse": 216, "Column2Reverse": 252,
						"Column3Reverse": 288, "Column4Reverse": 324},
	"LOOP_LOADER": {"PumpToColumn": 0, "PumpLoopToColumn": 45,
					"PumpToWaste": 90, "InjectToColumn": 270},
	"UNKNOWN_VALVE": {}}

rotaryValveTypes = {0: "UNKNOWN_VALVE",
					1: "BUFFER_SELECTOR",
					2: "COLUMN_SELECTOR",
					3: "LOOP_LOADER"}


class RotaryValve(PractichemSerialDevice):
	""" Control class for Practichem FluidSwitch valve

	This is the control class for the Practichem FluidSwitch family of valves.

	This class can be used by passing a setup SerialHandler or by using the
	more helpful DeviceManager class.

	Example of direct instantiation. Faster if you know the port.
	from practichem_rotary_valve import RotaryValve
	from practichem_device import SerialHandler

	serial_handler = SerialHandler()
	serial_handler.openPort("COM32")
	serial_handler.start()
	valve = RotaryValve(serial_handler)

	valve.jog(60)

	Example using the DeviceManager which is in the practichem_device package
	from practichem_device import DeviceManager
	import practichem_rotary_valve # required to register the product name

	device_manager = DeviceManager()
	valve = device_manager.getDeviceByProductName("RotaryValve")

	valve.jog(60)
	"""

	def __init__(self, serialHandler, valveType=None):
		if valveType:
			super().__init__("RotaryValve: " + valveType, serialHandler)
		else:
			super().__init__("RotaryValve: Unknown", serialHandler)
			valveType = self.getRotaryValveType()
		self.valveType = valveType
		self.valvePositionsInDegrees = rotaryValvePositionsInDegrees[self.valveType]

	def jogInSteps(self, stepsToJog):
		""" Rotate the valve some number of steps.
		:param stepsToJog: The number of motor steps to jog
		"""
		command = "rotaryValve,jogInSteps,{}".format(stepsToJog)
		self._performCommand(command, expectedResponse="SUCCESS")

	def jog(self, degreesToJog):
		""" Rotate the valve some number of degrees.
		:param degreesToJog: Degrees to rotate the valve, always rotates the shortest path
		"""
		command = "rotaryValve,jogInDegrees,{}".format(degreesToJog)
		self._performCommand(command, expectedResponse="SUCCESS")

	def selectPositionInDegrees(self, positionInDegrees):
		""" Rotate the valve to an absolute position in degrees.
		:param positionInDegrees: The destination in degrees to rotate the valve, valid values are 0 to 360
		"""
		assert (positionInDegrees > 0 and positionInDegrees <= 360)
		command = "rotaryValve,selectPositionInDegrees,{}".format(positionInDegrees)
		self._performCommand(command, expectedResponse="SUCCESS", timeoutInSeconds=12)

	def selectPosition(self, position):
		""" Rotate the valve to a named position.
		:param position: Name of the valve position to select
		:return:
		"""
		if position in self.valvePositionsInDegrees:
			newPositionInDegrees = self.valvePositionsInDegrees[position]
			self.selectPositionInDegrees(newPositionInDegrees)
		else:
			raise LookupError("Invalid valve position: {}".format(position))

	def setZeroPosition(self):
		""" Set the current position of the valve as the zero point.
		WARNING: Use only during calibration
		"""
		response = self._performCommand("rotaryValve,setZeroPosition", expectedResponse="SUCCESS")

	def getCurrentPositionInDegrees(self):
		""" Get the position of the valve in degrees.
		:return: Position in degrees
		"""
		return float(self._getParameter("rotaryValve", "positionInDegrees"))

	def getCurrentEncoderPosition(self):
		""" Get the current position as indicated by the encoder.
		:return: Position in encoder steps, range 0..4095
		"""
		return int(self._getParameter("rotaryValve", "encoderPosition"))

	def getLifetimeRotations(self):
		""" Get the cumulative rotation counter for the valve.
		:return: Cumulative rotations
		"""
		return int(self._getParameter("rotaryValve", "lifetimeRotations"))

	def resetLifetimeRotationCount(self):
		""" Reset the cumulative rotation count. """
		self._performCommand("rotaryValve,resetLifetimeRotations", expectedResponse="SUCCESS")

	def getRotaryValveType(self):
		""" Get the type of the rotary valve attached.
		This function directly queries the valve.
		"""
		valveType = self._getValveType()
		return rotaryValveTypes[valveType]

	def processMessage(self, message):
		super().processMessage(message)

	def _getValveType(self):
		""" Get the valve type index.
		:return: The rotary valve type index
		"""
		return int(self._getParameter("rotaryValve", "rotaryValveType"))

	def _getParameter(self, deviceName, parameterName, timeout=10):
		""" Get a named value from the valve. """
		command = "{},get{}".format(deviceName, parameterName)
		message = self._performCommand(command, expectedResponse=parameterName, timeoutInSeconds=timeout)
		return message[2]


class RotaryValveEmulator(PractichemEmulatorDevice):
	""" Emulates a RotaryValve.

	This class is useful for testing without access to a valve.

	See RotaryValve for function descriptions

	Example usage
	from practichem_rotary_valve import RotaryValveEmulator
	valve = RotaryValveEmulator()
	valve.jog(60)

	NOTE: Not all functionality is implemented.
	"""
	encoderStepsInRevolution = 4096
	encoderStepsInHalfRevolution = encoderStepsInRevolution / 2
	degreesInRevolution = 360
	fullRotationTimeInSeconds = 5

	def __init__(self, serialHandler, valveType=None):
		if not valveType:
			valveType = "BUFFER_SELECTOR"
		super().__init__("RotaryValve: " + valveType)
		self.currentPositionInEncoderSteps = 0
		self.valveType = valveType
		self.valvePositionsInDegrees = rotaryValvePositionsInDegrees[self.valveType]

	def _encoderStepsToDegrees(self, encoderSteps):
		return (encoderSteps / self.encoderStepsInRevolution) * self.degreesInRevolution

	def _degreesToEncoderSteps(self, degrees):
		return (degrees / self.degreesInRevolution) * self.encoderStepsInRevolution

	def jogInSteps(self, stepsToJog):
		logger.debug("Jogging {} steps".format(stepsToJog))
		self.currentPositionInEncoderSteps += stepsToJog

		# simulate the delay with 5 seconds to a complete turn
		sleep(self.fullRotationTimeInSeconds * (abs(stepsToJog) / self.encoderStepsInRevolution))

	def jog(self, degrees):
		self.jogInSteps(self._degreesToEncoderSteps(degrees))

	def selectPositionInDegrees(self, positionInDegrees):
		logger.info("Moving to position {} degrees".format(positionInDegrees))
		newEncoderPosition = self._degreesToEncoderSteps(float(positionInDegrees))
		logger.debug("Current Position {}".format(self.currentPositionInEncoderSteps))
		logger.debug("New Position {}".format(newEncoderPosition))
		stepsToMove = newEncoderPosition - self.currentPositionInEncoderSteps
		stepsToMove %= self.encoderStepsInRevolution
		# is the other direction shorter
		if stepsToMove > self.encoderStepsInHalfRevolution:
			stepsToMove = stepsToMove - self.encoderStepsInRevolution
		elif stepsToMove < -self.encoderStepsInHalfRevolution:
			stepsToMove = stepsToMove + self.encoderStepsInRevolution
		self.jogInSteps(stepsToMove)

	def selectPosition(self, position):
		if position in self.valvePositionsInDegrees:
			newPositionInDegrees = self.valvePositionsInDegrees[position]
			self.selectPositionInDegrees(newPositionInDegrees)
		else:
			raise LookupError("Invalid valve position: {}".format(position))

	def getCurrentPositionInDegrees(self):
		return float(self._encoderStepsToDegrees(self.currentPositionInEncoderSteps))

	def getCurrentEncoderPosition(self):
		return float(self.currentPositionInEncoderSteps)

	def getValveType(self):
		return self.valveType

	def setZeroPosition(self):
		pass

	def getRotaryValveType(self):
		return self.valveType
