import json

from stubserver import StubServer
import unittest

from simpletransfers import http, TransferException

test_json = json.dumps( { 'quantity': 5 } )

class testHTTP( unittest.TestCase ):

	def setUp(self):
		self.server = StubServer(8095)
		self.server.run()

	def tearDown(self):
		self.server.stop()

	def test_get(self):
		self.server.expect(
			method = "GET",
			url = "/mands/pin/serial/\d+$",
		).and_return(
			content = test_json,
			mime_type = "application/json",
		)

		obj = http( 'http://localhost:8095/mands/pin/serial/658329293232' )
		contents = obj.get()

		result = json.loads( contents[ '658329293232' ] )
		self.assertEquals( 5, result[ 'quantity' ] )

	def test_post(self):
		capture = {}
		self.server.expect(
			method = "POST",
			url = "/mands/serial",
			data_capture = capture,
		).and_return( reply_code = 200 )

		obj = http( 'http://localhost:8095/mands/serial' )
		obj.put( json.dumps( { 'quantity': 5 } ) )

		result = json.loads( capture[ 'body' ] )
		self.assertEquals( 5, result[ 'quantity' ] )

	def test_with_500(self):
		capture = {}
		self.server.expect(
			method = "POST",
			url = "/mands/allocate",
			data_capture = capture
		).and_return( reply_code = 500 )

		obj = http( 'http://localhost:8095/mands/allocate' )
		self.assertRaises( TransferException, obj.put, test_json )

if __name__ == '__main__':
	unittest.main()
