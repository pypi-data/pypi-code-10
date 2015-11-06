import re
import subprocess
import os

class ls(object):

	'''
		Iterator for listing all files in a directory.
		- Lists files found under path, unless <files> is False
		- Can also list directories, if <dirs> is True
		- Only files (and directories) matching <whitelist> 
			will be returned, unless they also match <blacklist>.
		- By default, doesn't descend into subdirectories, unless
			<recurse> is True, lists files in subdirs too.
		- If <recurse> is True, only directories matching <whitelist>
			and not matching <blacklist> will be followed
		- Paths to files are returned relative to <path>, unless <absolute>
			is true, then absolute paths are returned
		- Files are listed in natural sort ordering (i.e. respecting
			numerical order), but if <natural_sort> is False alphabetical
			order is used instead.
		- Hidden files (starting with '.') are ommitted, but if <list_all>
			is true, then they will be included.  In recursive mode, this
			is necessary in orderd to follow hidden  folders.
	'''

	def __init__(
		self,
		path,
		files=True,
		dirs=False,
		whitelist='.*',
		blacklist='^$',
		absolute=False,
		recurse=False,
		list_all=False,
		natural_sort=True,
	):
		self.path = path
		self.files = files
		self.dirs = dirs
		self.whitelist = re.compile(whitelist)
		self.blacklist = re.compile(blacklist)
		self.absolute = absolute
		self.recurse = recurse
		self.list_all = list_all
		self.natural_sort = natural_sort


	def filter_back_pointers(self, dirs):
		'''
			Exclude '.' and '..' from <dirs>.
		'''
		return filter(
			lambda i: not (i.split('/')[-1]=='.' or i.split('/')[-1]=='..'),
			dirs
		)


	def __iter__(self):
		self.yield_files, self.yield_dirs = self._ls(self.path)
		self.visit_dirs = list(self.yield_dirs)
		return self


	def next(self):
		'''
			yield the next item, and absolutize the path if necessary
		'''
		next_item = self.get_next()
		if self.absolute:
			return os.path.abspath(next_item)
		return next_item


	def get_next(self):

		while True:

			# Try popping off the next file, if we're yielding files
			if self.files:
				try:
					return self.yield_files.pop()
				except IndexError:
					pass

			# Try popping off the next dir, if we're yielding dirs
			if self.dirs:
				try:
					return self.yield_dirs.pop()
				except IndexError:
					pass

			# Try looking in the next dir
			if self.recurse:
				try:
					next_dir = self.visit_dirs.pop()
				except IndexError:
					raise StopIteration
				else:
					self.yield_files, self.yield_dirs = self._ls(next_dir)
					self.visit_dirs.extend(self.yield_dirs)

			# If not recursive, then we're done
			else:
				raise StopIteration


	def _ls(self, path, filter_back_pointers=True):

		# Ask OS to list the files and directories in path
		if self.list_all:
			list_command = ['ls', '-a', path]
		else:
			list_command = ['ls', path]
		ls = subprocess.Popen(list_command, stdout=subprocess.PIPE)


		# Sort the files and directories
		if self.natural_sort:
			sort_command = ['sort', '-n', '-r']
		else:
			sort_command = ['sort', '-r']
		items = subprocess.check_output(sort_command, stdin=ls.stdout)
		ls.wait()
		items = [os.path.join(path, i) for i in items.split()]

		# Get rid of '.' and '..', if necessary
		if self.list_all and filter_back_pointers:
			items = self.filter_back_pointers(items)

		# Go through the list separate files from directories
		files = []
		dirs = []
		for item in items:

			# Skip if it doesn't match whitelist, or does match blacklist
			if (
				not self.whitelist.search(item) 
				or self.blacklist.search(item)
			):
				continue

			# Append files to the list of files
			if os.path.isfile(item):
				files.append(item)

			# Append directories to the list of dirs
			else:
				dirs.append(item)

		return files, dirs

