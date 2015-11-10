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
import threading
import queue
import logging

import serial.tools.list_ports as list_ports

from practichem_device.serial_handler import SerialHandler, SerialPortLocked
from practichem_device.practichem_device import PractichemSerialDevice

logger = logging.getLogger(__name__)


portId = "port"
productNameId = "productName"
productNumberId = "productNumber"
serialNumberId = "serialNumber"
firmwareVersionId = "firmwareVersion"
firmwareBuildDateId = "firmwareBuildDate"
uuidId = "uuid"

deviceClassesByProductName = {}


def registerPractichemDeviceByProductName(productName, deviceClass):
	""" Register a control class to a product name.
	:param productName: The product name as reported by the device
	:param deviceClass: The class to instantiate for controlling the device
	"""
	deviceClassesByProductName[productName] = deviceClass


def getSerialHandlerForPort(port):
	""" Return a constructed and started SerialHandler for a port.
	:param port: A serial port name
	:return: A SerialHandler instance
	"""
	serialHandler = SerialHandler()
	serialHandler.openPort(port)
	serialHandler.start()
	return serialHandler


def getDeviceFromDeviceInformation(deviceInformation):
	""" Return the control class for a device from its information

	Requires the product name to be register with registerPractichemDeviceByProductName.
	Generally including the device package will register its device product name.
	:param deviceInformation: A dictionary of device information from DeviceManager
	:return: A constructed controller class for the device
	"""
	productName = deviceInformation[productNameId]
	if not productName in deviceClassesByProductName:
		raise Exception("Unregistered device productName: '{}'".format(productName))
	serialHandler = getSerialHandlerForPort(deviceInformation["port"])
	return deviceClassesByProductName[productName](serialHandler)


class DeviceQueryThread(threading.Thread):
	""" Support class for identifying the type of device on a port """
	timeoutInSeconds = 0.5

	def __init__(self, port, addDeviceCallback):
		threading.Thread.__init__(self)
		self.daemon = True
		self.port = port
		self.serialHandler = SerialHandler()
		self.messages = queue.Queue()
		self.addDeviceCallback = addDeviceCallback

	def run(self):
		try:
			self.serialHandler.openPort(self.port[0])
			self.serialHandler.start()
		except (SerialPortLocked, BlockingIOError) as exception:
			# ignore locked port errors, devices may already be open
			return
		except IOError:
			logger.exception("Failed to open port %s", self.port)
			return
		try:
			device = PractichemSerialDevice(None, self.serialHandler)
			deviceInfo = {portId: self.port[0]}
			deviceInfo[productNameId] = device.getProductName()
			deviceInfo[productNumberId] = device.getProductNumber()
			deviceInfo[firmwareVersionId] = device.getFirmwareVersion()
			deviceInfo[firmwareBuildDateId] = device.getFirmwareBuildDate()
			deviceInfo[uuidId] = device.getUuid()
			self.addDeviceCallback(deviceInfo)
		except (IOError, queue.Empty):
			# the device had a valid Practichem CDC VID:PID combination, failure means the device is not functioning
			logger.error("Practichem device not found on %s", self.port)
		finally:
			device.shutdown()
			# need to wait for the serial handler to shutdown to free the port, otherwise the
			# main application will fail trying to open the port
			self.serialHandler.join(10)


class DeviceManager(object):
	""" Class used for querying and connecting to devices.

	DeviceManager will automatically find all attached devices when
	it is created. To find devices attached after the DeviceManager is created
	call findDevices
	"""

	lock = threading.Lock()

	def __init__(self):
		""" Create an instance of DeviceManager
		Will automatically search for attached devices at creation time.
		"""
		self.informationForDevices = []
		self.findDevices()

	def findDevices(self):
		""" Search for Practichem devices """
		# prevent multiple simultaneous calls to findDevices
		with self.lock:
			self.informationForDevices = []
			# 2404 is the Atmel PID that is used for Practichem CDC devices
			ports = list_ports.grep("2404")
			deviceQueryThreadList = []
			for port in ports:
				logger.debug("Looking for device on port {}".format(port[0]))
				deviceQueryThread = DeviceQueryThread(port, self._add_device_callback)
				deviceQueryThread.start()
				deviceQueryThreadList.append(deviceQueryThread)

			# wait for all queries to finish
			for deviceQueryThread in deviceQueryThreadList:
				deviceQueryThread.join(5)

	def getInformationForAllDevices(self):
		def get_port(item):
			return item[portId]
		# sort the list by port so that it is consistent across calls
		return sorted(self.informationForDevices, key=get_port)

	def getInformationForMatchingDevices(self, **kwargs):
		"""
		Search for device using any combination of productName, productNumber, and uid
		"""
		informationForMatchingDevices = self.getInformationForAllDevices()
		if not kwargs:
			raise TypeError("Must specify a search type")
		if "productName" in kwargs:
			productName = kwargs["productName"]
			informationForMatchingDevices = [deviceInformation for deviceInformation in informationForMatchingDevices if
											 deviceInformation[productNameId] == productName]
		if "productNumber" in kwargs:
			productNumber = kwargs["productNumber"]
			informationForMatchingDevices = [deviceInformation for deviceInformation in informationForMatchingDevices if
											 deviceInformation[productNumberId] == productNumber]
		if "uid" in kwargs:
			uid = kwargs["uid"]
			# loosely match on uid, sometimes there is a leading space that could get lost
			informationForMatchingDevices = [deviceInformation for deviceInformation in informationForMatchingDevices if
											 uid in deviceInformation[uuidId]]
		return informationForMatchingDevices

	def getDeviceByProductName(self, productName):
		""" Return a device control class for a device with a matching product name.

		WARNING: If multiple devices with a matching product name are found,
		this function will return only one. Repeat calls to this function
		will not return different devices.
		:param productName: The product name to search for
		:return: A constructed device class
		"""
		informationForMatchingDevices = self.getInformationForMatchingDevices(productName=productName)
		if not informationForMatchingDevices:
			raise Exception("Device not found by productName: '{}'".format(productName))
		return getDeviceFromDeviceInformation(informationForMatchingDevices[0])

	def _add_device_callback(self, deviceInformation):
		""" Add device to found list """
		self.informationForDevices.append(deviceInformation)

def queryAndPrintDeviceList():
	""" Find all devices and print the list to the console """
	deviceManager = DeviceManager()
	informationForDevices = deviceManager.getInformationForAllDevices()
	if not informationForDevices:
		print("No devices found")
	else:
		for deviceInformation in informationForDevices:
			print(deviceInformation[productNameId])
			print("   Product Number:     ", deviceInformation[productNumberId])
			print("   UID:               ", deviceInformation[uuidId])
			print("   Firmware Build Date:", deviceInformation[firmwareBuildDateId])
			print("   Firmware Version:   ", deviceInformation[firmwareVersionId])
			print("   Port:               ", deviceInformation[portId])


# if run directly from the command line, print all of the devices and exit
if __name__ == "__main__":
	queryAndPrintDeviceList()
