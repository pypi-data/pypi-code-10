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
import logging
import time
from queue import Queue, Empty
from threading import Lock

logger = logging.getLogger(__name__)


def empty_queue(queue):
	""" Remove all items from the queue """
	while not queue.empty():
		try:
			queue.get(False)
		except Empty:
			continue


class CommunicationErrorException(Exception):
	""" An error has occurred while communicating with the device. """
	pass


class PractichemDevice(object):
	""" The base class for all Practichem device classes.

	Provides basic functionality for communicating with the device.
	Should not be used directly.
	"""

	# store a reference to each device so that devices can communicate with each other
	practichemDevices = {}

	def __init__(self, deviceName):
		"""
		:param deviceName: The device name to use for logging
		"""
		if deviceName:
			self.practichemDevices[deviceName] = self
		self.deviceName = deviceName
		self.serializers = []
		self.messages = Queue()
		self.waitingForResponse = False
		self.deviceCommunicationMutex = Lock()
		self.messageFromDeviceListeners = [self._messageErrorListener]

	def shutdown(self):
		""" Remove this device from the master device list. """
		try:
			del self.practichemDevices[self.deviceName]
		except KeyError:
			# ignore the error, most likely means that the shutdown command was called twice
			pass

	def getProductNumber(self):
		""" Return the product number of this device. """
		response = self._performCommand("module,getProductNumber", expectedResponse="productNumber")
		return response[2]

	def getProductName(self):
		""" Return the product name of this device. """
		response = self._performCommand("module,getProductName", expectedResponse="productName")
		return response[2]

	def getFirmwareVersion(self):
		""" Return the firmware version. """
		response = self._performCommand("module,getFirmwareVersion", expectedResponse="firmwareVersion")
		return response[2]

	def getFirmwareBuildDate(self):
		""" Return the build date of the firmware. """
		response = self._performCommand("module,getFirmwareBuildDate", expectedResponse="firmwareBuildDate")
		return response[2]

	def getUuid(self):
		""" Return the unique identifier for this device.
		The unique id is guareented to be unique across all Practichem devices.
		"""
		response = self._performCommand("module,getUuid", expectedResponse="uuid")
		return response[2]

	def rebootToBootloader(self):
		""" Reboot the device and enter the boot loader.
		Used for updating the firmware on the device.
		WARNING: Programming tool needed to return control to the firmware.
		A power cycle is insufficient to restore the device.
		"""
		self.sendMessageToDevice("module,rebootToBootloader")

	def getLogMessages(self):
		""" Return log messages from the device
		Each message will be separated by the newline character
		:return: A string of log messages
		"""
		return self._performCommand("module,getLogMessages", expectedResponse="logMessages")

	def addSerializer(self, serializer):
		""" Add a serializer to the device.
		Used internally by Practichem.
		"""
		self.serializers.append(serializer)

	def removeSerializer(self, serializer):
		""" Remove a serializer from the device """
		self.serializers.remove(serializer)

	def addMessageListener(self, callback):
		""" Add a function that will receive messages from this device.
		:param callback: A callable that takes one parameter, the message.
		"""
		self.messageFromDeviceListeners.append(callback)

	def removeMessageListener(self, callback):
		""" Stop a function from listening to messages """
		try:
			self.messageFromDeviceListeners.remove(callback)
		except ValueError:
			# ignore errors if the callback is not present
			pass

	def _performCommand(self, command, expectedResponse="", timeoutInSeconds=10):
		""" Send a command to the device and wait for result
		:param command: The string message to send to the device.
		"""
		self.deviceCommunicationMutex.acquire()
		try:
			# remove any old messages from the queue, otherwise it will look like a response from the device
			empty_queue(self.messages)
			self.waitingForResponse = True
			self.sendMessageToDevice(command)
			startTimeInSeconds = time.monotonic()
			while True:
				# how much time remains before the timeoutInSeconds is up
				timeRemainingInSeconds = timeoutInSeconds - (time.monotonic() - startTimeInSeconds)
				# now wait for response
				message = self.messages.get(timeout=timeRemainingInSeconds)
				self._checkResponse(message)
				# check to see if we received the message we expected, otherwise continue waiting
				if not expectedResponse or expectedResponse.lower() == message[1].lower():
					break
				else:
					# there may be other listeners waiting for this message
					self._notifyMessageListeners(message)
		finally:
			self.waitingForResponse = False
			# there may be more messages waiting in the queue behind the message we received
			self._notifyMessagesInQueue()
			self.deviceCommunicationMutex.release()
		return message

	def _notifyMessagesInQueue(self):
		"""
		Notify any listeners of messages that ended up in the message queue while waiting for performCommand
		"""
		while not self.messages.empty():
			message = self.messages.get()
			self._notifyMessageListeners(message)

	def _checkResponse(self, response):
		""" Check for errors in the response. """
		# all responses must have a device name and a message, example: ["device","SUCCESS"]
		if len(response) < 2:
			raise CommunicationErrorException("Error from {}: Message too short {}".format(response))
		elif response[1].upper() == "FAILED":
			raise CommunicationErrorException("Error from {}: {}".format(self.deviceName, response[2:]))

	def processMessage(self, message):
		""" Decode and route message from the device.
		:param message: Message from device
		:return: Decoded message
		"""
		# convert to normal string and split on comma
		messageParts = message.decode("ascii", "replace").split(',')

		if len(messageParts) > 2:
			if messageParts[1].upper() == "DEBUG":
				logger.debug("Debug message received from device: {}".format(messageParts[2:]))

		if self.waitingForResponse:
			self.messages.put(messageParts)
		else:
			self._notifyMessageListeners(messageParts)
		return messageParts

	def _notifyMessageListeners(self, message):
		""" Notify any listeners of received messages.
		Stops once a listener acknowledges the message by returning True
		"""
		for listener in self.messageFromDeviceListeners:
			messageHandled = listener(message)
			# allow a message handler to break the chain
			if messageHandled:
				break

	def _messageErrorListener(self, message):
		""" Report asynchronous errors to the serializers """
		if len(message) > 2:
			if message[1].upper() == "FAILED":
				for serializer in self.serializers:
					serializer.sendErrorMessage(message[2])
				return True

	def sendMessageToDevice(self, message):
		""" Send a message to the device. """
		raise NotImplementedError()


class PractichemSerialDevice(PractichemDevice):
	""" Base class for devices using a serial port or virtual port. """
	def __init__(self, deviceName, serialHandler):
		super().__init__(deviceName)
		self.serialHandler = serialHandler
		self.serialHandler.registerCallback(self.processMessage)

	def shutdown(self):
		super().shutdown()
		self.serialHandler.shutdown()

	def sendMessageToDevice(self, *messages):
		self.serialHandler.sendMessageToDevice(*messages)


class PractichemEmulatorDevice(PractichemDevice):
	""" Base class for emulated devices. """
	def __init__(self, deviceName):
		super().__init__(deviceName)

	def _performCommand(self, command, expectedResponse="", timeoutInSeconds=10):
		pass

	def sendMessageToDevice(self, message):
		pass

	def waitThenProcessSuccess(self, emulatedDeviceName, timeToWaitInSeconds, processMessage):
		logger.debug(timeToWaitInSeconds)
		time.sleep(timeToWaitInSeconds)
		processMessage(emulatedDeviceName + b",SUCCESS")


""" Tests """
def expect_exception(exception, function, *arguments, **kwargs):
	try:
		function(*arguments, **kwargs)
	except exception:
		return
	raise Exception("{} not raised".format(exception))

def test_perform_command():
	command = ""

	# just resend the value received
	def sendMessageToDevice(self, message):
		nonlocal command
		command = message
		self.processMessage(message)

	PractichemDevice.sendMessageToDevice = sendMessageToDevice
	device = PractichemDevice("Device")

	# test that the command is passed through
	device._performCommand(b"test,SUCCESS")
	assert command == b"test,SUCCESS"

	assert device._performCommand(b"test,response,1,2,3") == ["test","response","1","2","3"]
	assert device._performCommand(b"test,response,1", expectedResponse="response") == ["test","response","1"]

	# test timeout
	expect_exception(Empty, device._performCommand, b"test,test", expectedResponse="SUCCESS", timeoutInSeconds=1)

	print("test_perform_command SUCCESS")

if __name__ == "__main__":
	test_perform_command()
	#tests