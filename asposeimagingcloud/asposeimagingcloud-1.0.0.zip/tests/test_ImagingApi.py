import unittest
import os.path
import json
import inspect
import requests

import asposeimagingcloud
from asposeimagingcloud.ImagingApi import ImagingApi
from asposeimagingcloud.ImagingApi import ApiException
from asposeimagingcloud.models import ImagingResponse
from asposeimagingcloud.models import SaaSposeResponse

import asposestoragecloud 
from asposestoragecloud.StorageApi import StorageApi


class TestAsposeImagingCloud(unittest.TestCase):

    def setUp(self):

        with open('setup.json') as json_file:
            data = json.load(json_file)

        self.storageApiClient = asposestoragecloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.storageApi = StorageApi(self.storageApiClient)

        self.apiClient = asposeimagingcloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.imagingApi = ImagingApi(self.apiClient)

        self.output_path = str(data['output_location'])

    def testGetImageBmp(self):

        try:
            name =  "sample.bmp"
            bitsPerPixel = 24
            horizontalResolution = 300
            verticalResolution = 300
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetImageBmp(name, bitsPerPixel, horizontalResolution, verticalResolution)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
    
    def testPostImageBmp(self):

        try:
            name =  "sample.bmp"
            bitsPerPixel = 24
            horizontalResolution = 300
            verticalResolution = 300
            
            response = self.imagingApi.PostImageBmp(bitsPerPixel, horizontalResolution, verticalResolution, file='./data/' + name)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    
    def testGetCropImage(self):

        try:
            fileName = "aspose"
            name =  fileName + ".jpg"
            format = "png"
            x = 30
            y = 40
            width = 100
            height = 100
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetCropImage(name, format, x, y, width, height)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
    
    def testPostCropImage(self):

        try:
            fileName = "aspose"
            name =  fileName + ".jpg"
            format = "png"
            x = 30
            y = 40
            width = 100
            height = 100

            response = self.imagingApi.PostCropImage(format, x, y, width, height, file='./data/' + name)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetImageFrame(self):

        try:
            name =  "sample-multi.tif"
            frameId = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetImageFrame(name, frameId)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
                                        
    def testGetImageFrameProperties(self):

        try:
            name =  "TestDemo.tif"
            frameId = 0
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetImageFrameProperties(name, frameId)            

            self.assertIsInstance(response,ImagingResponse.ImagingResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testGetImageGif(self):

        try:
            name =  "sample.gif"

            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetImageGif(name)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
        
    def testPostImageGif(self):

        try:
            name =  "sample.gif"
            backgroundColorIndex = 255
            colorResolution = 7
            
            response = self.imagingApi.PostImageGif(file='./data/' + name)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testGetImageJpg(self):

        try:
            name =  "aspose.jpg"
            quality = 100
            compressionType = "progressive"
            
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetImageJpg(name, quality=quality, compressionType=compressionType)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testPostImageJpg(self):

        try:
            name =  "aspose.jpg"
            quality = 100
            compressionType = "progressive"            
            
            response = self.imagingApi.PostImageJpg(file = './data/' + name, quality=quality, compressionType=compressionType)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testGetImagePng(self):

        try:
            name =  "aspose_imaging_for_cloud.png"
            fromScratch = True
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            
            response = self.imagingApi.GetImagePng(name, fromScratch=fromScratch)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testPostImagePng(self):

        try:
            name =  "aspose_imaging_for_cloud.png"
            fromScratch = True
            
            response = self.imagingApi.PostImagePng(file='./data/' + name, fromScratch=fromScratch)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testGetImageProperties(self):

        try:
            name =  "demo.tif"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetImageProperties(name)            

            self.assertIsInstance(response,ImagingResponse.ImagingResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testGetImagePsd(self):

        try:
            name =  "sample.psd"
            channelsCount = 3
            compressionMethod = "rle"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetImagePsd(name, channelsCount=channelsCount, compressionMethod=compressionMethod)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testPostImagePsd(self):

        try:
            name =  "sample.psd"
            channelsCount = 3
            compressionMethod = "rle"
            
            response = self.imagingApi.PostImagePsd(file='./data/' + name, channelsCount=channelsCount, compressionMethod=compressionMethod)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testGetChangeImageScale(self):

        try:
            fileName = "aspose_imaging_for_cloud"
            name =  fileName + ".png"
            format = "jpg"
            newWidth = 200
            newHeight = 200
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetChangeImageScale(name, format, newWidth, newHeight)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testPostChangeImageScale(self):

        try:
            fileName = "aspose_imaging_for_cloud"
            name =  fileName + ".png"
            format = "jpg"
            newWidth = 200
            newHeight = 200
            
            response = self.imagingApi.PostChangeImageScale(format, newWidth, newHeight, file='./data/' + name)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testGetImageRotateFlip(self):

        try:
            fileName = "aspose"
            name =  fileName + ".jpg"
            format = "png"
            method = "Rotate180FlipX"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetImageRotateFlip(name, format, method)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testPostImageRotateFlip(self):

        try:
            fileName = "aspose"
            name =  fileName + ".jpg"
            format = "png"
            method = "Rotate180FlipX"
            
            response = self.imagingApi.PostImageRotateFlip(format, method, file = './data/' + name)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testGetImageSaveAs(self):

        try:
            fileName = "aspose"
            name =  fileName + ".jpg"
            format = "png"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetImageSaveAs(name, format)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testPostImageSaveAs(self):

        try:
            fileName = "aspose"
            name =  fileName + ".jpg"
            format = "png"
            
            response = self.imagingApi.PostImageSaveAs(format, file = './data/' + name)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testGetTiffToFax(self):

        try:
            name =  "TestDemo.tif"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetTiffToFax(name)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testPostProcessTiff(self):

        try:
            name =  "demo.tif"
            compression = "ccittfax3"
            resolutionUnit = "inch"
            bitDepth = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.PostProcessTiff(file='./data/' + name, compression=compression, resolutionUnit=resolutionUnit, bitDepth=bitDepth)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testPostTiffAppend(self):

        try:
            name =  "sample.tif"
            appendFile = "TestDemo.tif"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.storageApi.PutCreate(appendFile,'./data/' + appendFile)
                        
            response = self.imagingApi.PostTiffAppend(name, appendFile=appendFile)            
            
            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testGetUpdatedImage(self):

        try:
            
            fileName = "TestDemo"
            name =  fileName + ".tif"
            format = "png"
            x = 96
            y = 96
            newWidth = 300
            newHeight = 300
            rectWidth = 200
            rectHeight = 200
            rotateFlipMethod = ""
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.imagingApi.GetUpdatedImage(name, format, newWidth, newHeight, x, y, rectWidth, rectHeight, rotateFlipMethod)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

        
    def testPostImageSaveAs_ImagingApi_0(self):

        try:
            fileName = "TestDemo"
            name =  fileName + ".tif"
            format = "png"
            x = 96
            y = 96
            newWidth = 300
            newHeight = 300
            rectWidth = 200
            rectHeight = 200
            rotateFlipMethod = ""
            
            response = self.imagingApi.PostImageSaveAs_ImagingApi_0(format, newWidth, newHeight, x, y, rectWidth, rectHeight, rotateFlipMethod, file= './data/' + name)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex
                                                                                                        
if __name__ == '__main__':
    unittest.main()