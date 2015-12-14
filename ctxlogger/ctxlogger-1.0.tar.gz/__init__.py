import contextlib
import logging

# is this the first time we've been included?
if '_contexts' not in globals():
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
	"""
	Add current context information to an exception message,
	then throws an exception of the given type.

	exc_type - an Exception type that takes a single string argument
	message - the exception message string
	orig_exc - (py3) The original exception that this is replacing
	"""
	#if orig_exc:
	#	raise exc_type( format_context( message ) ) from orig_exc
	raise exc_type( format_context( message ) )

class ContextFormatter( logging.Formatter ):

	def __init__( self, fmt = None, datefmt = None, level = True, timestamp = True ):
		"""
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
