"""
Fields define one value within a record, and can be one of the following types:
integer, decimal, date, string or constant.
"""
import ctxlogger
import re
import time

from datetime import datetime
from decimal import Decimal, InvalidOperation

from . import ParseException

# regular expressions for validating types of strings
string_types = {
	# basic, errs on the side of being too lenient
	# don't want to reject valid addresses
	u'email': re.compile( r'^\S+@\S+\.\S+$' ),
}

## Parsing a field can optionally take a 'required' argument,
## Which controls whether to throw an exception if the field cannot
## be converted into the requested type

## Unparsing a field can optionally take a length argument,
## which cause the field to padded to that length.
## For the numerical types the zero_padded argument determines
## whether this padding is 0's or spaces.

## Extract an integer from raw field data
def parse_int( field, required = True, nonzero = False, positive = False, **kwargs ):
	try:
		value = int( field )
	except ( ValueError, TypeError ) as e:
		if not required:
			return None
		ctxlogger.exception(
			ParseException,
			u'Value "{}" is not an integer'.format( str(field) ),
			orig_exc = e
		)

	if nonzero and value == 0:
		ctxlogger.exception( ParseException, u'Value is zero' )
	if positive and value < 0:
		ctxlogger.exception( ParseException, u'Value is negative' )

	return value

## Convert an integer into raw field data
def unparse_int(
	value,
	length = None,
	zero_padded = True,
	**kwargs
):
	parse_int( value, **kwargs ) # re-use existing validation
	if zero_padded:
		return unparse_string( value, length, filler = 0, **kwargs )
	return unparse_string( value, length, **kwargs )

## Extract a decimal from raw field data
def parse_decimal( field, required = True, min_precision = None, max_precision = None, **kwargs ):
	if not min_precision and not max_precision:
		try: # in case we're using the same format spec for in and out
			min_precision = kwargs[ u'precision' ]
			max_precision = kwargs[ u'precision' ]
		except KeyError:
			pass

	try:
		val = Decimal( str(field) )
		exp = -(val.as_tuple()[2])
	except ( TypeError, InvalidOperation ) as e:
		if not required:
			return None
		ctxlogger.exception(
			ParseException,
			u'Could not parse "{}" as a decimal'.format( field ),
			orig_exc = e
		)

	if min_precision != None and min_precision > exp:
		ctxlogger.exception(
			ParseException,
			u'Minimum precision not met: {} < {}'.format( exp, min_precision )
		)
	if max_precision != None and max_precision < exp:
		ctxlogger.exception(
			ParseException,
			u'Maximum precision exceeded: {} > {}'.format( exp, max_precision )
		)
	return val

## Convert a decimal into raw field data
## The precision argument determines how many digits after the decimal point
## to include (padding is done after).
def unparse_decimal( value, length = None, precision = None, zero_padded = True, **kwargs ):
	decvalue = parse_decimal( value )
	try:
		decvalue = round( decvalue, precision )
	except TypeError: # precision is None, no rounding required
		pass
	if zero_padded:
		return unparse_string( decvalue, length, filler = 0, **kwargs )
	return unparse_string( decvalue, length, **kwargs )

## Extract a string from raw field data
def parse_string( field, required = True, strip_spaces = True, str_type = None, **kwargs ):

	value = None
	if field != None:
		value = str(field)
		if strip_spaces:
			value = value.strip()

	if required and not value:
		ctxlogger.exception(
			ParseException, u'Empty string for required value'
		)
	if str_type:
		try:
			if not string_types[ str_type ].match( value ):
				ctxlogger.exception(
					ParseException, u'Invalid {} format'.format( str(str_type) )
				)
		except KeyError as e:
			ctxlogger.exception(
				ParseException,
				u'Unrecognised string type: {}'.format( str(str_type) ),
				orig_exc = e
			)
	return value

## Convert a string into raw field data
def unparse_string( value, length = None, justify = u'right', filler = u' ', str_type = None, **kwargs ):

	strval = parse_string( value, str_type = str_type )

	if length == None:
		return strval

	strlen = len(strval)

	if justify == u'left':
		op = u'<'
	elif justify == u'center':
		op = u'^'
	elif justify == u'right':
		op = u'>'
	else:
		ctxlogger.exception(
			ParseException,
			u'Invalid justification "{}"'.format( str(justify) ),
		)

	fmt = u'{0:%s%s%d.%d}' % ( str(filler), op, length, length )
	try:
		return fmt.format( strval )
	except ValueError as e:
		ctxlogger.exception(
			ParseException,
			u'Invalid fill character "{}"'.format( str(filler) ),
			orig_exc = e
		)

## Extract a datetime object from raw field data
def parse_date( field, fmt, required = True ):
	value = parse_string( field, required )
	try:
		return datetime( *time.strptime( value, fmt )[:6] )
	except Exception as e:
		ctxlogger.exception( ParseException, str(e), orig_exc = e )

## Convert a datetime object into raw field data
def unparse_date( value, length = None, fmt = u'%c', **kwargs ):
	try:
		field = value.strftime( fmt )
	except Exception as e:
		ctxlogger.exception( ParseException, str(e), orig_exc = e )
	return unparse_string( field, length, **kwargs )

## Validate a constant value
def parse_constant( field, constant, required = True, **kwargs ):
	value = parse_string( field, required )

	if constant != value:
		if not required:
			return None

		ctxlogger.exception(
			ParseException,
			u'{} does not equal {}'.format( str(value), str(constant) ),
		)

	return constant

## Return the constant value
def unparse_constant( value, length, constant, **kwargs ):
	return unparse_string( constant, length, **kwargs )

## The field class wraps the above conversion functions,
## storing the details about a specific field in a record,
## such as the start and end points (for a fixed width field),
## or whether the field is required.

class field( object ):
	def __init__( self, start = None, end = None, length = None, **kwargs ):
		self.start = start
		self.end = end
		self.length = length
		if start != None and end != None:
			self.length = end - start
		self.flags = kwargs

	def get_field( self, record ):
		if self.end:
			if self.end > len( record ):
				if self.flags.get( u'required', True ):
					ctxlogger.exception(
						ParseException,
						u'Record too short ({} < {})'.format(
							len(record), self.end
						)
					)
				return None
			return record[self.start:self.end]
		return record[self.start:]

	def parse( self, record ):
		field = record
		# If we have a start set, then the field is a substring of the whole
		# record, so pull that out first
		if self.start != None:
			field = self.get_field( record )
		return self._parse( field, **self.flags )

	def unparse( self, value ):
		return self._unparse( value, self.length, **self.flags )

class int_field( field ):
	def _parse( self, *args, **kwargs ):
		return parse_int( *args, **kwargs )

	def _unparse( self, *args, **kwargs ):
		return unparse_int( *args, **kwargs )

class decimal_field( field ):
	def _parse( self, *args, **kwargs ):
		return parse_decimal( *args, **kwargs )

	def _unparse( self, *args, **kwargs ):
		return unparse_decimal( *args, **kwargs )

class string_field( field ):
	def _parse( self, *args, **kwargs ):
		return parse_string( *args, **kwargs )

	def _unparse( self, *args, **kwargs ):
		return unparse_string( *args, **kwargs )

class date_field( field ):
	def _parse( self, *args, **kwargs ):
		return parse_date( *args, **kwargs )

	def _unparse( self, *args, **kwargs ):
		return unparse_date( *args, **kwargs )

class constant_field( field ):
	def _parse( self, *args, **kwargs ):
		return parse_constant( *args, **kwargs )

	def _unparse( self, *args, **kwargs ):
		return unparse_constant( *args, **kwargs )
