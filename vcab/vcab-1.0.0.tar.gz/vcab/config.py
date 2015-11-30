import os
import json
from voidpp_tools.json_config import JSONConfigLoader

loader = JSONConfigLoader(__file__)

def load_config():
	return loader.load('vcab-config.json')

def load_absinthe_config():
	absinthe_data_dir = os.path.join(os.path.expanduser('~'), '.absinthe')
	config_data = None
	try:
		with open(os.path.join(absinthe_data_dir, 'config.json')) as f:
			config_data = json.load(f)
		return config_data['server']
	except Exception as e:
		raise
