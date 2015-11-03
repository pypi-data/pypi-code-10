import unittest
import os.path
import json
import inspect
import requests

import asposeocrcloud
from asposeocrcloud.OcrApi import OcrApi
from asposeocrcloud.OcrApi import ApiException
from asposeocrcloud.models import OCRResponse

import asposestoragecloud 
from asposestoragecloud.StorageApi import StorageApi


class TestAsposeOcrCloud(unittest.TestCase):

    def setUp(self):

        with open('setup.json') as json_file:
            data = json.load(json_file)

        self.storageApiClient = asposestoragecloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.storageApi = StorageApi(self.storageApiClient)

        self.apiClient = asposeocrcloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.ocrApi = OcrApi(self.apiClient)

        self.output_path = str(data['output_location'])

    def testGetRecognizeDocument(self):

        try:
            name =  "Sampleocr.bmp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.ocrApi.GetRecognizeDocument(name)
            
            self.assertIsInstance(response,OCRResponse.OCRResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
    
    def testPostOcrFromUrlOrContent(self):

        try:
            name =  "Sampleocr.bmp"
            
            response = self.ocrApi.PostOcrFromUrlOrContent(file = './data/' + name, language = "english")            
            
            self.assertIsInstance(response,OCRResponse.OCRResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

if __name__ == '__main__':
    unittest.main()