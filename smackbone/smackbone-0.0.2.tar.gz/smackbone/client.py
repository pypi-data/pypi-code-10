from websocket import create_connection
import json
from .json_rpc import JsonRpc

class Client:

	def __init__(self, url=None, target=None, log=None):
		self.target = target
		self.log = log
		self._log('Url:{}'.format(url))
		self.websocket = create_connection(url)
		self.jsonrpc = JsonRpc(self, self.websocket, log=log)

	def _log(self, *log_params):
		self.log.log(*log_params)

	def _on_notification(self, o):
		self._log('Received notification')

	def _on_request(self, o):
		self._log('Received request')
		method_name = o['method']
		method = getattr(self.target, method_name)
		parameter_dictionary = o['params']
		method(**parameter_dictionary)

	def notification(self, name, data):
		self.jsonrpc.notification(name, data)

	def request(self, name, data):
		self.jsonrpc.request(name, data)

	def close(self):
		self._close()

	def _recv(self):
		return self.websocket.recv()

	def _close(self):
		self.websocket.close()
		self.websocket = None

	def run_forever(self):
		while True:
			message_text = self._recv()
			self._log('Incoming message "{}"'.format(message_text))
			json_object = json.loads(message_text)
			self.jsonrpc.receive_object(json_object)
