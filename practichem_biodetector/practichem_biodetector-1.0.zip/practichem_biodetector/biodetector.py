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
from collections import defaultdict
import random
import logging
import struct

from practichem_device import PractichemSerialDevice, PractichemEmulatorDevice
from practichem_device import TimerThread

logger = logging.getLogger(__name__)


class Biodetector(PractichemSerialDevice):
	""" Control Practichem D3 detector.

	This is the control class for interfacing with a Practichem D3 detector.
	The D3 detector consists of a two wavelength absorbance meter,
	a conductivity meter, and a temperature probe.

	This class can be used by passing a setup SerialHandler or by using the
	more helpful DeviceManager class.

	Example of direct instantiation. Faster if you know the port.
	from practichem_biodetector import Biodetector
	from practichem_device import SerialHandler

	serial_handler = SerialHandler()
	serial_handler.openPort("COM32")
	serial_handler.start()
	biodetector = Biodetector(serial_handler)

	print(biodetector.getPrimaryAbsorbance())

	Example using the DeviceManager which is in the practichem_device package
	from practichem_device import DeviceManager
	import practichem_biodetector # required to register the product name

	device_manager = DeviceManager()
	biodetector = device_manager.getDeviceByProductName("BioDetector")

	print(biodetector.getPrimaryAbsorbance())
	"""

	features = ["absorbance01", "absorbance02", "conductivity", "temperature"]

	def __init__(self, serialHandler):
		super().__init__("Biodetector", serialHandler)
		self.callbackDictionary = defaultdict(list)
		self._registerCallbacks()
		self.parameters = {}

	def getPrimaryAbsorbance(self):
		""" Return the absorbance of the liquid in the primary flowcell in AU. """
		return float(self._performCommand("absorbance01,getAbsorbanceInAu", expectedResponse="absorbanceInAu")[2])

	def getSecondaryAbsorbance(self):
		""" Return the absorbance of the liquid in the secondary flowcell in AU. """
		return float(self._performCommand("absorbance02,getAbsorbanceInAu", expectedResponse="absorbanceInAu")[2])

	def getConductivityInMicroSiemensPerCentimeter(self):
		""" Return the measured conductivity in micro Siemens per centimeter. """
		return float(self._performCommand("conductivity,getConductivityInMicroSiemenPerCentimeter", expectedResponse="conductivityInMicroSiemenPerCentimeter")[2])

	def getTemperatureInCelcius(self):
		""" Return the temperature of the liquid in the flowcell. """
		return float(self._performCommand("temperature,getTemperatureInCelsius", expectedResponse="temperatureInCelsius")[2])

	def getPrimaryWavelengthInNanometers(self):
		""" Return the wavelength in nanometers of the primary flow cell. """
		return self._getWavelengthInNanometers("absorbance01")

	def getSecondaryWavelengthInNanometers(self):
		""" Return the wavelength in nanometers of the secondary flow cell. """
		return self._getWavelengthInNanometers("absorbance02")

	def setPrimaryWavelengthInNanometers(self, newWavelengthInNanometers):
		""" Change the wavelength reported by the detector for the primary wavelength.

		NOTE: Only changes the reported wavelength
		"""
		command = "absorbance01,setWavelengthInNanometers,{}".format(newWavelengthInNanometers)
		self._performCommand(command, expectedResponse="SUCCESS")

	def setSecondaryWavelengthInNanometers(self, newWavelengthInNanometers):
		""" Change the wavelength reported by the detector for the secondary wavelength.

		NOTE: Only changes the reported wavelength
		"""
		command = "absorbance02,setWavelengthInNanometers,{}".format(newWavelengthInNanometers)
		self._performCommand(command, expectedResponse="SUCCESS")

	def getRawPrimaryAbsorbanceInCounts(self):
		""" Return the sensor value for the primary absorbance

		The sensor value for absorbance corresponds to the amount of light
		transmitted through the cell.
		Output range is 0 to 25165824.
		The value 16777216 is roughly zero received light
		"""
		return int(self._performCommand("absorbance01,getUncalibratedAbsorbance", expectedResponse="uncalibratedAbsorbance")[2])

	def getRawSecondaryAbsorbanceInCounts(self):
		""" Return the sensor value for the secondary absorbance

		See getRawPrimaryAbsorbanceInCounts for more details.
		"""
		return int(self._performCommand("absorbance02,getUncalibratedAbsorbance", expectedResponse="uncalibratedAbsorbance")[2])

	def getRawConductivityInCounts(self):
		""" Return the sensor value for the conductivity

		The raw sensor value as recorded by the ADC. Does not include
		temperature or cell constant compensation.
		Output range is from 0 to 16777215.
		"""
		return int(self._performCommand("conductivity,getUncalibratedConductivity", expectedResponse="uncalibratedConductivity")[2])

	def getRawTemperatureInCounts(self):
		""" Return the sensor value for the temperature

		The raw sensor value as recorded by the ADC.
		Output range is from 0 to 8191.
		"""
		return int(self._performCommand("temperature,getUncalibratedTemperature", expectedResponse="uncalibratedTemperature")[2])

	def startMeasuring(self):
		""" Enable the UV LEDs. """
		return self._sendCommandToAllFeatures("startMeasuring")

	def stopMeasuring(self):
		""" Disable the UV LEDs. """
		return self._sendCommandToAllFeatures("stopMeasuring")

	def startStreaming(self):
		""" Start sending readings from the Biodetector. """
		return self._sendCommandToAllFeatures("startStreamingData")

	def stopStreaming(self):
		""" Stop sending readings from the Biodetector. """
		return self._sendCommandToAllFeatures("stopStreamingData")

	def startRawStreaming(self):
		""" Start sending raw/uncalibrated readings from the biodetector. """
		return self._sendCommandToAllFeatures("startStreamingUncalibratedData")

	def stopRawStreaming(self):
		""" Stop sending raw/uncalibrated readings from the biodetector. """
		return self._sendCommandToAllFeatures("stopStreamingUncalibratedData")

	def getUvLedState(self):
		""" Return the current state of the UV LEDS.

		Valid states are:
		DISABLED - The UV LEDs are currently off and may be enabled with startMeasuring
		ENABLED - The UV LEDs are currently on and may be disabled with stopMeasuring
		DISABLED_DUE_TO_LOCKOUT - The UV LEDs are disabled because ambient light was detected in the emitter cover.
			Replace the emitter cover before attempting to enable the UV LEDs with startMeasuring.
		"""
		return self._performCommand("absorbance01,getUvLedState", expectedResponse="uvLedState")[2]

	def getUvLedOnTimeInMinutes(self):
		""" Return the cumulative UV LED on time in minutes. """
		return float(self._performCommand("absorbance01,getUvLedOnTimeInMinutes", expectedResponse="uvLedOnTimeInMinutes")[2])

	def calibrateAbsorbanceMeters(self):
		# todo: this function does  nothing at present
		self._performCommand("absorbance01,calibrateAbsorbance", expectedResponse="SUCCESS")

	def zeroAbsorbanceMeters(self):
		""" Zero the absorbance at the current value. """
		self._performCommand("absorbance01,zeroAbsorbance", expectedResponse="SUCCESS")

	def sendConductanceCalibration(self, conductivityInMicroSiemensPerCentimeter):
		""" Calibrate the conductivity using the passed conductivity as the reference. """
		command = "conductivity,setConductivity,{}".format((float(conductivityInMicroSiemensPerCentimeter)))
		self._performCommand(command, expectedResponse="SUCCESS")

	def getParameterValue(self, parameterName):
		""" Return the newest valve for a instrument by name. """
		try:
			return self.parameters[parameterName]
		except KeyError:
			return 0

	def registerFeatureCallback(self, callback, featureName=""):
		""" Register a callback for receipt of new data from a feature.

		If featureName is not specified then the callback will be called for all messages from the device
		"""
		self.callbackDictionary[featureName].append(callback)

	def unregisterFeatureCallback(self, callback):
		""" Unregister a callback that was previously registered with registerFeatureCallback. """
		for feature in self.callbackDictionary:
			if callback in self.callbackDictionary[feature]:
				self.callbackDictionary[feature].remove(callback)

	# WARNING: The following functions are for factory use only and may cause a device to become inoperable if used in correctly
	def getValuesFromNonVolatileStorage(self, callback=None):
		""" Return the calibration and other parameters that are stored in the device.

		NOTE: debugging function, does not return data in a user accessible way.
		"""
		if callback:
			self.registerFeatureCallback(callback, "module")
		return self._performCommand("module,getParameters", expectedResponse="parameterList")

	def eraseNonVolatileStorage(self):
		""" Erase the contents of the nonvolatile memory on the device.

		NOTE: Debugging function only, will permanently delete all calibration data.
		"""
		self._performCommand("module,eraseEEPROM", expectedResponse="SUCCESS")

	def setValueInNonVolatileStorage(self, key, value):
		""" Set the value of a parameter by index value. """
		self._performCommand("module,setParameter,{},{}".format(key, value), expectedResponse="SUCCESS")

	def setValueInNonVolatileStorageAsFloat(self, key, value):
		""" Set the value of a parameter by index value using a floating point number. """
		# this code is equivalent to the c integer = *(uint32_t *)&floatingPointValue
		# convert the float to its byte representation
		byteInterpretation = struct.pack("f", value)
		# convert that byte representation to a unsigned integer to send to the detector
		packedValue = struct.unpack("I", byteInterpretation)[0]
		self.setValueInNonVolatileStorage(key, packedValue)

	def saveChangesToNonVolatileStorage(self):
		""" Save the changes to values to nonvolatile storage.

		If this is not called then changes will be lost on a loss of power
		"""
		self._performCommand("module,saveParameters", expectedResponse="SUCCESS")

	def _addParameterValue(self, parameterName, value):
		""" Add a value from the device to the parameters list. """
		self.parameters[parameterName] = value

	def _getWavelengthInNanometers(self, devicename):
		""" Return the wavelength for a specific device. """
		command = "{},getWavelengthInNanometers".format(devicename)
		response = self._performCommand(command, expectedResponse="wavelengthInNanometers")
		return int(response[2])

	def processMessage(self, message):
		""" Process a message received from the device. """
		messages = super().processMessage(message)

		# callbacks not associated with any particular feature
		if "" in self.callbackDictionary:
			for callback in self.callbackDictionary[""]:
				callback(messages[:])

		if messages[0] in self.callbackDictionary:
			for callback in self.callbackDictionary[messages[0]]:
				callback(messages[:])

	def _sendCommandToAllFeatures(self, message):
		""" Send a message to all features of the device. """
		for feature in self.features:
			self._performCommand("{},{}".format(feature, message), expectedResponse="SUCCESS")

	def _generalParameterCallback(self, messages):
		""" Convert the messages from the device into parameters and store them in the parameter list. """
		if len(messages) > 2:
			if messages[1] != 'FAILED':
				# build a tuple of the device name and the parameter name
				parameter = (messages[0], messages[1])
				if messages[1] in ["absorbanceInAu", "uncalibratedAbsorbance", "conductivityInMicroSiemenPerCentimeter", "uncalibratedConductivity",
								   "temperatureInCelsius", "uncalibratedTemperature"]:
					try:
						value = float(messages[2])
						self._addParameterValue(parameter, value)
					except ValueError:
						logger.exception("Cannot convert {} to float".format(messages[2]))

	def _registerCallbacks(self):
		""" Register all of the feature callbacks used by the class """
		self.registerFeatureCallback(self._generalParameterCallback, "absorbance01")
		self.registerFeatureCallback(self._generalParameterCallback, "absorbance02")
		self.registerFeatureCallback(self._generalParameterCallback, "conductivity")
		self.registerFeatureCallback(self._generalParameterCallback, "temperature")


class BiodetectorEmulator(PractichemEmulatorDevice):
	""" Emulate the Biodetector class.

	This class is useful for testing code without having access to a D3.

	Example usage
	from practichem_biodetector import BiodetectorEmulator
	biodetector = BiodetectorEmulator()
	print(biodetector.getPrimaryAbsorbance())

	NOTE: Not all functionality is implemented.
	"""
	
	absorbance1Key = ("absorbance01", "absorbanceInAu")
	absorbance2Key = ("absorbance02", "absorbanceInAu")
	conductivityKey = ("conductivity", "conductivityInMicroSiemenPerCentimeter")
	temperatureKey = ("temperature", "temperatureInCelsius")

	def __init__(self, serial_handler=""):
		super().__init__("BiodetectorEmulator")
		self.parameters = {}
		self.parameters[self.absorbance1Key] = 0
		self.parameters[self.absorbance2Key] = 0
		self.parameters[self.conductivityKey] = 0
		self.parameters[self.temperatureKey] = 25
		self.streamTimer = None

	def startMeasuring(self):
		logger.info("startMeasuring")

	def stopMeasuring(self):
		logger.info("startMeasuring")

	def getPrimaryAbsorbance(self):
		return self.parameters[self.absorbance1Key]

	def getSecondaryAbsorbance(self):
		return self.parameters[self.absorbance2Key]

	def getConductivityInMicroSiemensPerCentimeter(self):
		return self.parameters[self.conductivityKey]

	def getTemperatureInCelcius(self):
		return self.parameters[self.temperatureKey]

	def getPrimaryWavelengthInNanometers(self):
		return 280

	def getSecondaryWavelengthInNanometers(self):
		return 260

	def setPrimaryWavelengthInNanometers(self, newWavelengthInNanometers):
		logger.info("setPrimaryWavelengthInNanometers to {}".format(newWavelengthInNanometers))

	def setSecondaryWavelengthInNanometers(self, newWavelengthInNanometers):
		logger.info("setSecondaryWavelengthInNanometers to {}".format(newWavelengthInNanometers))

	def getRawPrimaryAbsorbanceInCounts(self):
		return 12345678

	def getRawSecondaryAbsorbanceInCounts(self):
		return 23456789

	def getRawConductivityInCounts(self):
		return 202020

	def getRawTemperatureInCounts(self):
		return 2000

	def startStreaming(self):
		self.stopStreaming()
		self.streamTimer = TimerThread(self.updateMeasurements, 0.5)
		self.streamTimer.start()

	def stopStreaming(self):
		if self.streamTimer is not None:
			self.streamTimer.stop()
			self.streamTimer = None

	def startRawStreaming(self):
		# NOTE: Not currently implemented
		pass

	def stopRawStreaming(self):
		# NOTE: Not currently implemented
		pass

	def getUvLedState(self):
		return "ENABLED"

	def getUvLedOnTimeInMinutes(self):
		return 1000

	def updateMeasurements(self):
		self.parameters[self.absorbance1Key] += random.uniform(-0.001, 0.001)
		self.parameters[self.absorbance2Key] += random.uniform(-0.001, 0.001)
		self.parameters[self.conductivityKey] += random.uniform(-0.01, 0.01)
		self.parameters[self.temperatureKey] += random.uniform(-0.001, 0.001)

	def zeroAbsorbanceMeters(self):
		self.parameters[self.absorbance1Key] = 0
		self.parameters[self.absorbance2Key] = 0

	def registerFeatureCallback(self, callback, featureName=""):
		pass

	def unregisterFeatureCallback(self, callback):
		pass

	def getParameterValue(self, parameterName):
		""" Return the newest valve for a instrument by name. """
		try:
			return self.parameters[parameterName]
		except KeyError:
			return 0
