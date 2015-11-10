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
import serial
import weakref
from practichem_device.weak_callback import WeakCallable

try:
	# try to use fcntl so that the serial port can be locked, only supported on Linux
	import fcntl
	use_file_locking = True
except ImportError:
	use_file_locking = False

import logging
logger = logging.getLogger(__name__)

MESSAGE_START_CHARACTER = b'\x02'  # STX
MESSAGE_END_CHARACTER = b'\x03'  # ETX
MESSAGE_ESCAPE_CHARACTER = b'\x10'  # DLE

MESSAGE_START = b'\x10\x02'
MESSAGE_END = b'\x10\x03'
MESSAGE_ESCAPED_BYTES = b'\x10\x10'
MESSAGE_ESCAPED_BYTES_REPLACEMENT = b'\x10'


class SerialException(Exception):
	pass


class SerialPortLocked(Exception):
	pass


class SerialHandler(threading.Thread):
	""" Handles communication with a device over a serial port.

	To use create an instance of the class and call openPort with the same of a serial port.
	Call the start method to begin the receiving loop in a new thread.
	"""
	open_ports = set()
	open_ports_lock = threading.RLock()

	def __init__(self): # pylint: disable=super-on-old-class
		""" Construct a serial handler class. """
		super().__init__()
		# do not block the program closing
		self.daemon = True
		self.escapeNextCharacter = False
		self.messageBuffer = bytearray()
		self.shouldShutdown = False
		self.serialPortWriteLock = threading.RLock()
		self.callbackLock = threading.RLock()
		self.receiveDataCallbacks = []
		self.receivingMessage = False
		self.serialPort = None
		self.serialPortName = None

	def registerCallback(self, callback):
		""" Register a callback method for incoming messages from the device.
		The callback is called with one parameter which is a bytes object of the message.
		"""
		with self.callbackLock:
			self.receiveDataCallbacks.append(WeakCallable(callback, callback=self._unregisterCallback))

	def unregisterCallback(self, callback):
		""" Unregister a callback to stop receiving messages """
		with self.callbackLock:
			self.receiveDataCallbacks.remove(WeakCallable(callback))

	def shutdown(self):
		""" Shutdown communications and close the serial port.
		Due to threading the serial port may take several seconds to close. """
		self.shouldShutdown = True

	def openPort(self, serialPortName):
		""" Open the serial port given by serialPortName.
		Throws serial.SerialException on error.
		"""
		with self.open_ports_lock:
			if serialPortName in self.open_ports:
				raise SerialPortLocked("{} is already open".format(serialPortName))

			self.serialPort = serial.Serial(serialPortName, 115200, timeout=1, writeTimeout=1)
			# Linux allows multiple programs to access the serial port, lock it to prevent multiple access
			if use_file_locking:
				try:
					fcntl.flock(self.serialPort.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
				except OSError as exception:
					self.serialPort.close()
					self.serialPort = None
					raise SerialPortLocked(exception.what())
			self.serialPortName = serialPortName
			self.open_ports.add(serialPortName)

	def runWithoutThreading(self):
		""" Start the message loop synchronously.
		Does not launch a new thread.
		This function blocks until the message loop returns with shutdown() or
		an error is thrown.
		"""
		self._messageLoop()

	def sendMessageToDevice(self, *messages):
		""" Send a message to the connected device.
		Takes a variable length argument of
		bytes, bytebuffer, or str. Handles escaping input as needed.
		"""
		if self.shouldShutdown is True or not self.serialPort:
			raise SerialException("Port closed")
		with self.serialPortWriteLock:
			try:
				messageToDevice = bytearray()
				messageToDevice.extend(MESSAGE_ESCAPE_CHARACTER + MESSAGE_START_CHARACTER)
				for message in messages:
					# convert to bytes
					if isinstance(message, str):
						message = bytes(message.encode("ascii"))
					# escape DLE characters by sending them twice
					message = message.replace(MESSAGE_ESCAPE_CHARACTER, MESSAGE_ESCAPE_CHARACTER + MESSAGE_ESCAPE_CHARACTER)
					messageToDevice.extend(message)
				messageToDevice.extend(MESSAGE_ESCAPE_CHARACTER + MESSAGE_END_CHARACTER)
				if len(messageToDevice) % 64 == 0:
					# fholton: messages that are multiples of 64 bytes stall the USB messages
					# just add an empty message that gets ignored
					messageToDevice.extend(MESSAGE_START + MESSAGE_END)
				self.serialPort.write(messageToDevice)
				self.serialPort.flush()
			except serial.serialutil.SerialException as exception:
				raise SerialException(exception)

	def run(self):
		""" Run the message loop.
		Called by the Thread on start()
		"""
		self._messageLoop()

	def _unregisterCallback(self, weakMethod):
		with self.callbackLock:
			self.receiveDataCallbacks.remove(weakMethod)

	def _messageLoop(self):
		""" Wait for messages from the serial port and process them. """
		try:
			while not self.shouldShutdown:
				# If there are other bytes waiting read them all in one call, reduces overhead of calling read for every byte.
				characters = self.serialPort.read(self.serialPort.inWaiting() or 1)
				if characters:
					self._processCharacters(characters)
		except serial.SerialException as exception:
			raise SerialException(exception)
		finally:
			self._closePort()
			self._shutdown()

	def _processCharacters(self, characters):
		""" Parse characters received from the device. """
		self.messageBuffer.extend(characters)

		# loop in case there is more than one message in the buffer
		while 1:
			end = self.messageBuffer.find(MESSAGE_END)
			while end > 0:
				if self.messageBuffer[end - 1] == b"\x10"[0]:
					# found escaped delimiter try again
					end = self.messageBuffer.find(MESSAGE_END, end+1)
				else:
					break
			if end >= 0:
				start = self.messageBuffer.rfind(MESSAGE_START, 0, end)

				while start > 0:
					if self.messageBuffer[start - 1] == b"\x10"[0]:
						# found escaped delimiter
						start = self.messageBuffer.rfind(MESSAGE_START, 0, start)
					else:
						break
				if start >= 0:
					if start > 0:
						logger.error("Found {} before start of message".format(self.messageBuffer[0:start]))
					# found a message
					message = self.messageBuffer[start+2:end]
					message = message.replace(MESSAGE_ESCAPED_BYTES, MESSAGE_ESCAPED_BYTES_REPLACEMENT)
					self._processMessage(message)
					# remove the message from the buffer, including anything before the start marker
					self.messageBuffer = self.messageBuffer[end+2:]
				else:
					# found an end with no start before it, remove it and log the fragment
					logger.error("Found {} with no start".format(self.messageBuffer[0:end]))
					self.messageBuffer = self.messageBuffer[end+2:]
			else:
				break

	def _processMessage(self, message):
		""" Process a complete message from the device and then call callbacks. """
		with self.callbackLock:
			for callback in self.receiveDataCallbacks:
				# create a copy of the message so that callbacks cannot modify the original message
				try:
					callback()(message[:])
				except TypeError:
					logger.error("Callback destroyed without dropping reference: {}".format(callback))
				except Exception: # pylint: disable=broad-except
					# log and ignore exceptions from callbacks, callbacks should not crash serial thread
					logger.exception("Exception occurred in callback")

	def _closePort(self):
		self.serialPort.close()
		with self.open_ports_lock:
			self.open_ports.discard(self.serialPortName)

	def _shutdown(self):
		self.serialPort = None
		self.messageBuffer = None


""" Testing """
def testProcessCharacters():
	serialHandler = SerialHandler()
	messages = []
	def processMessage(message):
		messages.append(message)
	def testMessage(message, expectedMessages):
		serialHandler.messageBuffer = bytearray()
		messageWithDelimiters = b"\x10\x02" + message + b"\x10\x03"
		messages.clear()
		serialHandler._processCharacters(messageWithDelimiters)
		try:
			for expectedMessage in expectedMessages:
				returnedMessage = messages.pop(0)
				if returnedMessage != expectedMessage:
					raise Exception("{} != {}".format(returnedMessage, expectedMessage))
			if messages:
				raise Exception("{} found after last expected message".format(messages.pop()))
		except IndexError:
			raise Exception("Expected message missing, messageBuffer = {}".format(serialHandler.messageBuffer))
	serialHandler._processMessage = processMessage

	testMessage(b"module,hello,world", [b"module,hello,world"])
	testMessage(b"module,\x10\x10,!@#$%^&*()_+", [b"module,\x10,!@#$%^&*()_+"])
	testMessage(b"", [b""])
	# fragmented message, it should ignore the fragment and use the last complete message
	testMessage(b"module,\x10\x10,!@#$%^&*()_+\x10\x02\x10\x03", [b""])
	testMessage(b"abcd\x10\x02", [b""])
	testMessage(b"abcd\x10\x02\x10\x03\x10\x02message", [b"", b"message"])
	testMessage(b"message1\x10\x03\x10\x03\x10\x02message2", [b"message1", b"message2"])

	# test escape sequences
	testMessage(b"\x10\x10\x03\x02", [b"\x10\x03\x02"])
	testMessage(b"\x10\x10\x02\x03", [b"\x10\x02\x03"])

	serialHandler.messageBuffer = bytearray()
	serialHandler._processCharacters(b"\x10\x03")
	assert len(messages) == 0

	serialHandler.messageBuffer = bytearray()
	serialHandler._processCharacters(b"\x10\x02")
	assert len(messages) == 0

	print("Success: testProcessCharacters")

def testRegisterMessage():
	serialHandler = SerialHandler()
	messages = []
	def callback(message):
		messages.append(message)
	serialHandler.registerCallback(callback)
	def testCallback(message):
		messages.clear()
		serialHandler._processCharacters(b"\x10\x02" + message + b"\x10\x03")
		assert messages.pop(0) == message

	def testUnregister(message):
		messages.clear()
		serialHandler._processCharacters(b"\x10\x02" + message + b"\x10\x03")
		assert len(messages) == 0

	testCallback(b"testing")
	serialHandler.unregisterCallback(callback)
	testUnregister(b"testing")

	print("Success: testRegisterMessage")

def testSendMessageToDevice():
	serialHandler = SerialHandler()
	messages = []
	class FakeSerialPort(object):
		def write(self, message):
			messages.append(message)
		def flush(self):
			pass

	serialHandler.serialPort = FakeSerialPort()

	def testWrite(message, expectedMessage):
		serialHandler.sendMessageToDevice(message)

		sentMessage = messages.pop(0)
		if expectedMessage != sentMessage:
			raise Exception("{} != {}".format(sentMessage, expectedMessage))
		if messages:
			raise Exception("Found {} after message".format(messages.pop))

	testWrite(b"", b"\x10\x02\x10\x03")
	testWrite(b"message", b"\x10\x02message\x10\x03")
	testWrite(b"\x10", b"\x10\x02\x10\x10\x10\x03")
	print("Success: testSendMessageToDevice")

if __name__ == "__main__":
	testProcessCharacters()
	testRegisterMessage()
	testSendMessageToDevice()
