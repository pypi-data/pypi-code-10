class Storage:
	def __init__ (self, f):
		raise Exception ('This is an interface')

	def __getitem__(self, key):
		raise Exception ('This is an interface')
		
	def __setitem__(self, key, value):
		raise Exception ('This is an interface')
		
	def __contains__(self, key):
		raise Exception ('This is an interface')

	def sync (self):
		raise Exception ('This is an interface')
		

    
