"""Miscellaneous functions that could be useful when interacting with the SynapsePay API"""
import base64
import mimetypes
import requests


def file_to_base64(**kwargs):
	"""
	Converts a file path into a correctly padded base64 representation
	for the SynapsePay API.  Mimetype padding is done by file 
	extension not by content(for now).
	
	Args:
	    **kwargs: file_path
	
	Returns:
	    TYPE: Base64 representation of the file.
	"""
	file_path = kwargs.get('file_path')
	with open(file_path, 'wb') as file_object:
		encoded_string = base64.b64encode(file_object.read())
		mime_type = mimetypes.guess_type(file_object.name)[0]
		mime_padding = 'data:' + mime_type + ';base64,'
		base64_string = mime_padding + encoded_string
		return base64_string

def url_to_base64(**kwargs):
	"""
	Converts a url into a correctly padded base64 representation
	for the SynapsePay API.  Mimetype padding is done by file 
	extension not by content(for now).
	
	Args:
	    **kwargs: url
	
	Returns:
	    TYPE: Base64 representation of the file.
	"""
	url = kwargs.get('url')
	response = requests.get(url)
	mime_type = mimetypes.guess_type(url)[0]
	uri = ("data:" + mime_type + ";" +"base64," + base64.b64encode(response.content))
	return uri
