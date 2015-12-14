import contextlib
import logging
import six # need for exception chaining

# is this the first time we've been included?
if u'_contexts' not in globals():
	_contexts = []
	separator = u' // '

def push_context( context, value ):
	global _contexts
	_contexts.append( ( context, value, ) )

def pop_context():
	global _contexts
	try:
		_contexts.pop()
	except IndexError:
		raise IndexError( u'ctxlogger - pop called on empty context' )

@contextlib.contextmanager
def context( context, value ):
	push_context( context, value )
	try:
		yield
	finally:
		pop_context()

def format_context( message ):
	fields = []
	fields += [ u'%s: %s' % ( c[0], c[1] ) for c in _contexts ]
	fields.append( message )
	return separator.join( fields )

def exception( exc_type, message, orig_exc = None ):
	u"""
	Add current context information to an exception message,
	then throws an exception of the given type.

	exc_type - an Exception type that takes a single string argument
	message - the exception message string
	orig_exc - The original exception that this is replacing
	"""
	six.raise_from( exc_type( format_context( message ) ), orig_exc )

class ContextFormatter( logging.Formatter ):

	def __init__( self, fmt = None, datefmt = None, level = True, timestamp = True ):
		u"""
		fmt - passed to logging.Formatter
		datefmt - passed to logging.Formatter
		level - include %(levelname)s in output? (default: True)
		timestamp - include %(asctime)s in output? (default: True)
		"""
		self.include_level = level
		self.include_timestamp = timestamp
		super( ContextFormatter, self ).__init__( fmt, datefmt )

	def format( self, record ):
		fields = []
		if self.include_timestamp:
			fields.append( u'timestamp: %(asctime)s' )
		if self.include_level:
			fields.append( u'level: %(levelname)s' )
		fields.append( format_context( u'%(message)s' ) )

		self._fmt = separator.join( fields )
		return super( ContextFormatter, self ).format( record )
