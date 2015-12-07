import json

class JsonRpc:

	def __init__(self, target, stream, log=None):
		self.stream = stream
		self.target = target
		self.log = log
		self.request_id = 0

	def _log(self, *log_params):
		self.log.log(*log_params)

	def receive_object(self, json_object):
		self._debug_output('Incoming', json_object)
		version = json_object['json-rpc']
		self._log('version:', version)
		if version != '2.0':
			raise Exception('Wrong version')
		del json_object['json-rpc']
		if 'id' in json_object:
			self._on_request(json_object)
		elif 'method' in json_object:
			self._on_notification(json_object)

	def notification(self, name, data):
		event_object = {'method': name, 'params': data}
		self._send_rpc_object(event_object)

	def request(self, name, data):
		self.request_id += 1
		request_object = {'method': name, 'params': data, 'id':self.request_id}
		self._send_rpc_object(request_object)

	def _send(self, text):
		self.stream.send(text)

	def _send_object(self, o):
		self._debug_output('send object', o)
		output = json.dumps(o, sort_keys=True, indent=4)
		self._send(output)

	def _debug_output(self, description, json_object):
		output = json.dumps(json_object, sort_keys=True, indent=4)
		self._log('{}: "{}"'.format(description, output))

	def _send_rpc_object(self, o):
		self._debug_output('rpc', o)
		o['json-rpc'] = '2.0'
		self._send_object(o)

	def _on_request(self, json_object):
		self._debug_output('on_request', json_object)
		self.target._on_request(json_object)

	def _on_notification(self, json_object):
		self._debug_output('on_request', json_object)
		self.target._on_notification(json_object)
