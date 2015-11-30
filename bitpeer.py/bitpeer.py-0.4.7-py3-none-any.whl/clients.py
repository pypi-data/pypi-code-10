import binascii
from io import BytesIO
from .serializers import *
from pycoin.block import Block
from .exceptions import NodeDisconnectException, InvalidMessageChecksum
import os
import codecs

class ProtocolBuffer (object):
	def __init__ (self):
		self.buffer = BytesIO()
		self.header_size = MessageHeaderSerializer.calcsize()
		#self.socket = socket

	def write (self, data):
		self.buffer.write(data)

	def receive_message (self):
		"""This method will attempt to extract a header and message.
		It will return a tuple of (header, message) and set whichever
		can be set so far (None otherwise).
		"""
		# Calculate the size of the buffer
		self.buffer.seek(0, os.SEEK_END)
		buffer_size = self.buffer.tell()

		# Check if a complete header is present
		if buffer_size < self.header_size:
			return (None, None)

		# Go to the beginning of the buffer
		self.buffer.seek(0)

		message_model = None
		message_header_serial = MessageHeaderSerializer()
		message_header = message_header_serial.deserialize(self.buffer)
		total_length = self.header_size + message_header.length

		# Incomplete message
		if buffer_size < total_length:
			self.buffer.seek(0, os.SEEK_END)
			return (message_header, None)

		payload = self.buffer.read(message_header.length)
		#print (codecs.encode (payload, 'hex'))
		remaining = self.buffer.read()
		self.buffer = BytesIO()
		self.buffer.write(remaining)
		payload_checksum = MessageHeaderSerializer.calc_checksum(payload)

		# Check if the checksum is valid
		if payload_checksum != message_header.checksum:
			msg = "Bad checksum for command %s" % message_header.command
			raise InvalidMessageChecksum(msg)

		if message_header.command in MESSAGE_MAPPING:
			#print (message_header.command)
			if message_header.command == 'block':
				message_model = Block.parse(BytesIO(payload))
				#print (message_model.id ())
			else:
				deserializer = MESSAGE_MAPPING[message_header.command]()
				message_model = deserializer.deserialize(BytesIO(payload))

		return (message_header, message_model)

class ChainBasicClient (object):
	"""The base class for a Bitcoin network client, this class
	implements utility functions to create your own class.

	:param socket: a socket that supports the makefile()
				   method.
	"""
	def __init__(self, socket, chain = 'BTC'):
		if not networks.isSupported (chain):
			 raise networks.UnsupportedChainException ()

		self.chain = chain.upper ()
		self.socket = socket
		self.buffer = ProtocolBuffer()
		self.run = True

	def stop (self):
		self.run = False
		time.sleep (5)
		if self.socket != None:
			self.socket.close ()

	def update_socket (self, socket):
		self.socket = socket

	def close_stream(self):
		"""This method will close the socket stream."""
		self.socket.close()

	def handle_message_header(self, message_header, payload):
		"""This method will be called for every message before the
		message payload deserialization.

		:param message_header: The message header
		:param payload: The payload of the message
		"""
		pass

	def handle_send_message(self, message_header, message):
		"""This method will be called for every sent message.

		:param message_header: The header of the message
		:param message: The message to be sent
		"""
		pass


	def send_tx (self, message):
		bin_data = BytesIO()
		message_header = MessageHeader(self.chain)
		message_header_serial = MessageHeaderSerializer()

		bin_message = binascii.unhexlify (message)
		payload_checksum = MessageHeaderSerializer.calc_checksum(bin_message)
		message_header.checksum = payload_checksum
		message_header.length = len(bin_message)
		message_header.command = 'tx'

		bin_data.write(message_header_serial.serialize(message_header))
		bin_data.write(bin_message)
		self.socket.sendall(bin_data.getvalue())
		self.handle_send_message(message_header, message)


	def send_message(self, message):
		"""This method will serialize the message using the
		appropriate serializer based on the message command
		and then it will send it to the socket stream.

		:param message: The message object to send
		"""
		bin_data = BytesIO()
		message_header = MessageHeader(self.chain)
		message_header_serial = MessageHeaderSerializer()

		serializer = MESSAGE_MAPPING[message.command]()
		bin_message = serializer.serialize(message)
		payload_checksum = \
			MessageHeaderSerializer.calc_checksum(bin_message)
		message_header.checksum = payload_checksum
		message_header.length = len(bin_message)
		message_header.command = message.command

		bin_data.write(message_header_serial.serialize(message_header))
		bin_data.write(bin_message)

		self.socket.sendall(bin_data.getvalue())
		self.handle_send_message(message_header, message)


	def loop(self):
		"""This is the main method of the client, it will enter
		in a receive/send loop."""

		while self.run:
			data = self.socket.recv(1024*8)

			if len(data) <= 0:
				raise NodeDisconnectException("Node disconnected")

			self.buffer.write(data)
			message_header, message = self.buffer.receive_message()

			if message_header is not None:
				self.handle_message_header(message_header, data)

			if not message:
				continue

			handle_func_name = "handle_" + message_header.command
			handle_func = getattr(self, handle_func_name, None)
			if handle_func:
				handle_func(message_header, message)


class ChainClient(ChainBasicClient):
	"""This class implements all the protocol rules needed
	for a client to stay up in the network. It will handle
	the handshake rules as well answer the ping messages."""

	def handshake(self):
		"""This method will implement the handshake of the
		Bitcoin protocol. It will send the Version message."""
		version = Version()
		self.send_message(version)

	def handle_version(self, message_header, message):
		"""This method will handle the Version message and
		will send a VerAck message when it receives the
		Version message.

		:param message_header: The Version message header
		:param message: The Version message
		"""
		verack = VerAck()
		self.send_message(verack)

	def handle_ping (self, message_header, message):
		"""This method will handle the Ping message and then
		will answer every Ping message with a Pong message
		using the nonce received.

		:param message_header: The header of the Ping message
		:param message: The Ping message
		"""
		pong = Pong()
		pong.nonce = message.nonce
		self.send_message(pong)
