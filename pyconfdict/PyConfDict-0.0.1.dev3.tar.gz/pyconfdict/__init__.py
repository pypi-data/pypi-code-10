from __future__ import print_function, division
import collections
import json

class PyConfDict(collections.OrderedDict):

	def __init__(self,*args,json_fn=None,**kwargs):
		if json_fn is not None:
			super(self.__class__,self).__init__({})
			self.update_from_json(json_fn,allow_new_keys=True)
		else:
			super(self.__class__,self).__init__(*args,**kwargs)

	def update(self,conf_dict,allow_new_keys=False):
		"""Update dictionary from another dictionary.
		"""
		old_keys=self.keys()
		super(self.__class__, self).update(conf_dict)
		new_keys=self.keys()
		if not allow_new_keys:
			if old_keys!=new_keys:
				raise ValueError("Adding new keys during update ({})".format(
						", ".join(new_keys-old_keys))
					)

	def update_from_json(self,json_fn,allow_new_keys=False):
		"""Update from a JSON file.
		"""
		with open(json_fn) as json_fo:
			conf_dict=json.loads(json_fo.read())
		self.update(conf_dict=conf_dict,allow_new_keys=allow_new_keys)
			
	def fill_missing(self,conf_dict):
		"""Add (key,value) for missing keys.
		"""

		new_pcd=PyConfDict(conf_dict)
		new_pcd.update(self)
		for key in new_pcd.keys():
			self[key]=new_pcd[key]
	
	def fill_missing_from_json(self,json_fn):
		"""Fill missing values from a JSON file.
		"""
		with open(json_fn) as json_fo:
			conf_dict=json.loads(json_fo.read())
		self.fill_missing(conf_dict=conf_dict,allow_new_keys=allow_new_keys)

	def save_to_json(self,json_fn):
		"""Save to a JSON file.
		"""
		with open(json_fn,"w+") as json_fo:
			json.dump(self,json_fo,sort_keys=False, indent=4)

