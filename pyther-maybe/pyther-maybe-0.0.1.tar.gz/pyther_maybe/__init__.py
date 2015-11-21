"""
This library implements the Either and Maybe semantic that is common in typed languages with sum types.

This provides a more robust way to encode failure or the absentence of values than None or exceptions.

'pythonic' is a cancer and just waiting to go wrong, exceptions for flow control are a very silly concept
they should only be used to deal with an exceptional state of the world the program can't enforce or indicate programming errors

for instance, if you want to modify a global variable in a function, you don't have to use the nasty global keyword:

global_var = Maybe()

def function ( arg ):
	global_var[Value] = new_value

if global_var: # test if it has been set
	print global_var[Value] # read the value
"""

__version__ = '0.0.1'

_unique = object() # this is a unique implementation detail constructed which compares singularly to itself

class EitherException      (Exception): pass
class RightEitherException (Exception): pass
class LeftEitherException  (Exception): pass

class Either ():

	"""
	A way to encode a value not being there. Either(<value>) encodes a (right) value
	where Either(left=<error>) encodes a value not being there with <error> providing possible info on why (or simply being None)
	
	It also functions as an iterator which either contains 1 or no value depending on if the "right side" is set.
	
	It can also be subscripted, where subscripting it with a truth value will access the right side and and a false value the left one
	Note that because 0 and 1 are truthy and falsy they can be used
	
	The structure of course counts as having length 0, and thus falsy if the left side is set and not the right side
	"""
	
	def __init__ ( self, right = _unique, left = _unique ):
		if right is _unique:
			if left is _unique: left = None
		else:
			if left is not _unique:
				raise TypeError("Either right or left must have a value, never both")
		
		self._right = right
		self._left  = left
	
	def right ( self, right = _unique ):
		"""
		use this to obtain or set the right value
		when a value is given, it is set, otherwise, it is accessed
		"""
		if right is _unique:
			if self:
				return self._right
			else:
				raise RightEitherException
		else:
			self._left  = _unique
			self._right = right
	
	def left ( self, left = _unique ):
		"""
		use this to obtain or set the left value
		when a value is given, it is set, otherwise,it is accssed
		"""
		if left is _unique:
			if not self:
				return self._left
			else:
				raise LeftEitherException
		else:
			self._right = _unique
			self._left  = left
			
	def either ( self, either = _unique ):
		"""
		this either accesses whichever field is currently used if no argument is given
		or sets the other one, if one is given
		"""
		if either is _unique:
			return self[self]
		else:
			self[not self] = either
	
	def extract ( self, callback = exit ):
		if self:
			return self.right()
		else:
			return callback(self.left())

	def is_right ( self ):
		"""
		test if the right side is set
		"""
		return bool(self)
	
	def is_left ( self ):
		"""
		test if the left side is set
		"""
		return (not self)
	
	def __getitem__ ( self, key ):
		if key:
			return self.right()
		else:
			return self.left()
	
	def __setitem__ ( self, key, value ):
		if key:
			self.right(value)
		else:
			self.left(value)
	
	def __delitem__ ( self, key ):
		if key:
			if self:
				self.left(None)
			else:
				raise RightEitherException
		else:
			if not self:
				self.right(None)
			else:
				raise RightEitherException
	
	def __iter__ ( self ):
		if self._right is not _unique:
			yield self._right
	
	def __len__ ( self ):
		return sum(1 for _ in self)
	
	__call__ = right



# convenience functions
def right ( value ):
	"""
	simply make an Either whose right field is set
	"""
	return Either(value)

def left ( value ):
	"""
	simply make an Either whose right left is set
	"""
	return Either(left=value)

# more idiomatic keys:
Right = True
Left  = False

class Maybe(Either):

	"""
	A variant of Either where the left side is always simply None when set
	Useful when you don't need to encode information
	"""
	
	def __init__ ( self, right = _unique, left = _unique ):
		if not (left is _unique or left is None):
			raise TypeError("argument to left must be None")
		Either.__init__(self, right=right, left=left)
	
	def value ( self, value = _unique ):
		"""
		just an alias for Maybe.right
		"""
		return Maybe.right(self, value)
	
	def is_value ( self ):
		"""
		just an alias for Maybe.is_right
		"""
		return Maybe.is_right(self)
		
	
	def nothing ( self, value = _unique ):
		"""
		just an alias for Maybe.left
		almost completely useless but here for consistency
		"""
		return Maybe.left(self, value)
	
	def is_nohing ( self ):
		"""
		just an alias for Maybe.is_left
		"""
		return Maybe.is_nothing(self)
		
	def left ( self, left = _unique):
		"""
		use this to obtain or set the left value
		when a value is given, it is set, otherwise,it is accssed
		
		Enforces the extra constraint that the value must be None
		"""
		if not (left is _unique or left is None):
			raise TypeError("argument to left must be None")
		return Either.left(self, left)

# convenience functions
def value ( value ):
	"""
	simply make a Maybe with a value
	"""
	return Maybe(value)
	
def nothing():
	"""
	simply make a maybe without a value
	"""
	return Maybe()

# more idiomatic keys:
Value   = Right
Nothing = Left
