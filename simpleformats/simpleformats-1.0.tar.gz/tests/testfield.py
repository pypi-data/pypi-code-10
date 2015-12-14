import time
import unittest
from datetime import datetime
from decimal import Decimal

from .. import ParseException
from ..field import (
	parse_int,
	unparse_int,
	parse_decimal,
	unparse_decimal,
	parse_string,
	unparse_string,
	parse_date,
	unparse_date,
	parse_constant,
	unparse_constant,
	field,
	int_field,
	decimal_field,
	string_field,
	constant_field,
)

class testIntField( unittest.TestCase ):

	def test_parse_valid( self ):
		output = parse_int( u'10' )
		self.assertEqual( output, 10 )

	def test_parse_invalid( self ):
		self.assertRaises( ParseException, parse_int, u'wibble' )
		output = parse_int( u'wibble', required = False )
		self.assertEqual( output, None )

	def test_parse_nonzero( self ):
		output = parse_int( -2, nonzero = True )
		self.assertEqual( output, -2 )

	def test_parse_nonzero_fail( self ):
		self.assertRaises( ParseException, parse_int, 0, nonzero = True )

	def test_parse_positive( self ):
		output = parse_int( 2, positive = True )
		self.assertEqual( output, 2 )

	def test_parse_positive_fail( self ):
		self.assertRaises( ParseException, parse_int, -2, positive = True )

	def test_unparse_valid( self ):
		output = unparse_int( 10 )
		self.assertEqual( output, u'10' )

	def test_unparse_with_length( self ):
		output = unparse_int( 10, 5 )
		self.assertEqual( output, u'00010' )

	def test_unparse_with_length_spaces( self ):
		output = unparse_int( 10, 5, zero_padded = False )
		self.assertEqual( output, u'   10' )

class testDecimalField( unittest.TestCase ):

	def test_parse( self ):
		output = parse_decimal( u'10.48' )
		self.assertEqual( output, Decimal( u'10.48' ) )

	def test_parse_invalid( self ):
		self.assertRaises( ParseException, parse_decimal, u'wibble' )
		output = parse_decimal( u'wibble', required = False )
		self.assertEqual( output, None )

	def test_parse_precision_min( self ):
		self.assertRaises(
			ParseException,
			parse_decimal, u'10.48', precision = 3,
		)

	def test_parse_precision_max( self ):
		self.assertRaises(
			ParseException,
			parse_decimal, u'10.48', precision = 1,
		)

	def test_parse_min_precision( self ):
		self.assertRaises(
			ParseException,
			parse_decimal, u'10.48', min_precision = 3,
		)

	def test_parse_max_precision( self ):
		self.assertRaises(
			ParseException,
			parse_decimal, u'10.48', max_precision = 1,
		)

	def test_unparse( self ):
		output = unparse_decimal( 10.48 )
		self.assertEqual( output, u'10.48' )

	def test_unparse_invalid( self ):
		self.assertRaises( ParseException, unparse_decimal, u'wibble' )

	def test_unparse_length_and_precision( self ):
		output = unparse_decimal( 10.48, 5, 1 )
		self.assertEqual( output, u'010.5' )

	def test_unparse_length_spaces( self ):
		output = unparse_decimal( 10.48, 7, zero_padded = False )
		self.assertEqual( output, u'  10.48' )

class testStringField( unittest.TestCase ):

	def test_parse( self ):
		output = parse_string( u'wibble' )
		self.assertEqual( output, u'wibble' )

	def test_parse_fail( self ):
		self.assertRaises( ParseException, parse_string, u'' )
		output = parse_string( u'', required = False )
		self.assertEqual( output, u'' )

	def test_parse_email( self ):
		output = parse_string( u'wibble@bob.com', str_type = u'email' )
		self.assertNotEqual( output, None )

	def test_parse_email_fail( self ):
		self.assertRaises(
			ParseException,
			parse_string, u'wibble', str_type = u'email',
		)
		self.assertRaises(
			ParseException,
			parse_string, u'wibble@bob', str_type = u'email',
		)

	def test_unparse( self ):
		output = unparse_string( u'wibble' )
		self.assertEqual( output, u'wibble' )

	def test_unparse_with_length( self ):
		output = unparse_string( u'wibble', 8 )
		self.assertEqual( output, u'  wibble' )

	def test_unparse_left_justify( self ):
		output = unparse_string( u'wibble', 8, justify = u'left' )
		self.assertEqual( output, u'wibble  ' )

	def test_unparse_center_justify( self ):
		output = unparse_string( u'wibble', 8, justify = u'center' )
		self.assertEqual( output, u' wibble ' )

	def test_unparse_alt_filler( self ):
		output = unparse_string( u'wibble', 8, filler = '.' )
		self.assertEqual( output, u'..wibble' )

	def test_unparse_truncate( self ):
		output = unparse_string( u'wibble', 3 )
		self.assertEqual( output, u'wib' )

	def test_unparse_email( self ):
		output = unparse_string( u'wibble@bob.com', str_type = u'email' )
		self.assertEqual( output, u'wibble@bob.com' )

	def test_unparse_email_fail( self ):
		self.assertRaises(
			ParseException,
			unparse_string, u'wibble@bob', str_type = u'email',
		)

class testDateField( unittest.TestCase ):
	def test_parse( self ):
		output = parse_date( u'2015-04-01 13:00:56', u'%Y-%m-%d %H:%M:%S'  )
		self.assertEqual(
			output,
			datetime( 2015, 4, 1, 13, 0, 56 )
		)

	def test_parse_invalid( self ):
		self.assertRaises(
			ParseException,
			parse_date, u'wibble@bob', u'%Y-%m-%d %H:%M:%S'
		)

	def test_unparse( self ):
		output = unparse_date(
			datetime( 2015, 4, 1, 14, 0, 15 ),
			fmt = u'%Y-%m-%d %H:%M:%S',
		)
		self.assertEqual( output, u'2015-04-01 14:00:15' )

	def test_unparse_invalid( self ):
		self.assertRaises( ParseException, unparse_date, u'not a date' )

class testConstantField( unittest.TestCase ):
	def test_constant( self ):
		output = parse_constant( u'aaaa', u'aaaa' )
		self.assertEqual( output, u'aaaa' )
		self.assertRaises( ParseException, parse_constant, u'aaaa', u'bbbb' )

		output = unparse_constant( None, 4, u'aaaa' )
		self.assertEqual( output, u'aaaa' )

		obj = constant_field( constant = u'aaaa' )
		output = obj.parse( u'aaaa' )
		self.assertEqual( output, u'aaaa' )
		self.assertRaises( ParseException, obj.parse, ( u'bbbb' ) )

		output = obj.unparse( None )
		self.assertEqual( output, u'aaaa' )

class testFieldObject( unittest.TestCase ):
	def test_field( self ):
		fobj = field()
		self.assertEqual( fobj.get_field( u'0123456789' ), u'0123456789' )

		fobj = field( 0, 4 )
		self.assertEqual( fobj.get_field( u'0123456789' ), u'0123' )
		self.assertRaises( ParseException, fobj.get_field, u'012' )

if __name__ == u'__main__':
	unittest.main()
