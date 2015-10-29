#!/usr/bin/env python

import sys
import os
import urllib
import json
import re
from models import *
from ApiClient import ApiException


class ImagingApi(object):

    def __init__(self, apiClient):
      self.apiClient = apiClient

    

    def GetImageBmp(self, name, bitsPerPixel, horizontalResolution, verticalResolution, **kwargs):
        """Update parameters of bmp image.
        Args:
            name (str): Filename of image. (required)

            bitsPerPixel (int): Color depth. (required)

            horizontalResolution (int): New horizontal resolution. (required)

            verticalResolution (int): New vertical resolution. (required)

            fromScratch (bool): Specifies where additional parameters we do not support should be taken from. If this is true 
            
            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'bitsPerPixel', 'horizontalResolution', 'verticalResolution', 'fromScratch', 'outPath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetImageBmp" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/bmp/?appSid={appSid}&amp;bitsPerPixel={bitsPerPixel}&amp;horizontalResolution={horizontalResolution}&amp;verticalResolution={verticalResolution}&amp;fromScratch={fromScratch}&amp;outPath={outPath}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'bitsPerPixel' in allParams and allParams['bitsPerPixel'] is not None:
            resourcePath = resourcePath.replace("{" + "bitsPerPixel" + "}" , str(allParams['bitsPerPixel']))
        else:
            resourcePath = re.sub("[&?]bitsPerPixel.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'horizontalResolution' in allParams and allParams['horizontalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "horizontalResolution" + "}" , str(allParams['horizontalResolution']))
        else:
            resourcePath = re.sub("[&?]horizontalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'verticalResolution' in allParams and allParams['verticalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "verticalResolution" + "}" , str(allParams['verticalResolution']))
        else:
            resourcePath = re.sub("[&?]verticalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fromScratch' in allParams and allParams['fromScratch'] is not None:
            resourcePath = resourcePath.replace("{" + "fromScratch" + "}" , str(allParams['fromScratch']))
        else:
            resourcePath = re.sub("[&?]fromScratch.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostImageBmp(self, bitsPerPixel, horizontalResolution, verticalResolution, file, **kwargs):
        """Update parameters of bmp image.
        Args:
            bitsPerPixel (int): Color depth. (required)

            horizontalResolution (int): New horizontal resolution. (required)

            verticalResolution (int): New vertical resolution. (required)

            fromScratch (bool): Specifies where additional parameters we do not support should be taken from. If this is true

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['bitsPerPixel', 'horizontalResolution', 'verticalResolution', 'fromScratch', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostImageBmp" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/bmp/?appSid={appSid}&amp;bitsPerPixel={bitsPerPixel}&amp;horizontalResolution={horizontalResolution}&amp;verticalResolution={verticalResolution}&amp;fromScratch={fromScratch}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'bitsPerPixel' in allParams and allParams['bitsPerPixel'] is not None:
            resourcePath = resourcePath.replace("{" + "bitsPerPixel" + "}" , str(allParams['bitsPerPixel']))
        else:
            resourcePath = re.sub("[&?]bitsPerPixel.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'horizontalResolution' in allParams and allParams['horizontalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "horizontalResolution" + "}" , str(allParams['horizontalResolution']))
        else:
            resourcePath = re.sub("[&?]horizontalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'verticalResolution' in allParams and allParams['verticalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "verticalResolution" + "}" , str(allParams['verticalResolution']))
        else:
            resourcePath = re.sub("[&?]verticalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fromScratch' in allParams and allParams['fromScratch'] is not None:
            resourcePath = resourcePath.replace("{" + "fromScratch" + "}" , str(allParams['fromScratch']))
        else:
            resourcePath = re.sub("[&?]fromScratch.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetCropImage(self, name, format, x, y, width, height, **kwargs):
        """Crop existing image
        Args:
            name (str): The image name. (required)

            format (str): Output file format. Valid Formats: Bmp, png, jpg, tiff, psd, gif. (required)

            x (int): X position of start point for cropping rectangle (required)

            y (int): Y position of start point for cropping rectangle (required)

            width (int): Width of cropping rectangle (required)

            height (int): Height of cropping rectangle (required)

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'format', 'x', 'y', 'width', 'height', 'outPath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetCropImage" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/crop/?appSid={appSid}&amp;toFormat={toFormat}&amp;x={x}&amp;y={y}&amp;width={width}&amp;height={height}&amp;outPath={outPath}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'x' in allParams and allParams['x'] is not None:
            resourcePath = resourcePath.replace("{" + "x" + "}" , str(allParams['x']))
        else:
            resourcePath = re.sub("[&?]x.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'y' in allParams and allParams['y'] is not None:
            resourcePath = resourcePath.replace("{" + "y" + "}" , str(allParams['y']))
        else:
            resourcePath = re.sub("[&?]y.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'width' in allParams and allParams['width'] is not None:
            resourcePath = resourcePath.replace("{" + "width" + "}" , str(allParams['width']))
        else:
            resourcePath = re.sub("[&?]width.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'height' in allParams and allParams['height'] is not None:
            resourcePath = resourcePath.replace("{" + "height" + "}" , str(allParams['height']))
        else:
            resourcePath = re.sub("[&?]height.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostCropImage(self, format, x, y, width, height, file, **kwargs):
        """Crop image from body
        Args:
            format (str): Output file format. Valid Formats: Bmp, png, jpg, tiff, psd, gif. (required)

            x (int): X position of start point for cropping rectangle (required)

            y (int): Y position of start point for cropping rectangle (required)

            width (int): Width of cropping rectangle (required)

            height (int): Height of cropping rectangle (required)

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['format', 'x', 'y', 'width', 'height', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostCropImage" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/crop/?appSid={appSid}&amp;toFormat={toFormat}&amp;x={x}&amp;y={y}&amp;width={width}&amp;height={height}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'x' in allParams and allParams['x'] is not None:
            resourcePath = resourcePath.replace("{" + "x" + "}" , str(allParams['x']))
        else:
            resourcePath = re.sub("[&?]x.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'y' in allParams and allParams['y'] is not None:
            resourcePath = resourcePath.replace("{" + "y" + "}" , str(allParams['y']))
        else:
            resourcePath = re.sub("[&?]y.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'width' in allParams and allParams['width'] is not None:
            resourcePath = resourcePath.replace("{" + "width" + "}" , str(allParams['width']))
        else:
            resourcePath = re.sub("[&?]width.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'height' in allParams and allParams['height'] is not None:
            resourcePath = resourcePath.replace("{" + "height" + "}" , str(allParams['height']))
        else:
            resourcePath = re.sub("[&?]height.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetImageFrame(self, name, frameId, **kwargs):
        """Get separate frame of tiff image
        Args:
            name (str): Filename of image. (required)

            frameId (int): Number of frame. (required)

            newWidth (int): New width of the scaled image. (optional)

            newHeight (int): New height of the scaled image. (optional)

            x (int): X position of start point for cropping rectangle (optional)

            y (int): Y position of start point for cropping rectangle (optional)

            rectWidth (int): Width of cropping rectangle (optional)

            rectHeight (int): Height of cropping rectangle (optional)

            rotateFlipMethod (str): RotateFlip method.(Rotate180FlipNone, Rotate180FlipX, Rotate180FlipXY, Rotate180FlipY,             Rotate270FlipNone, Rotate270FlipX, Rotate270FlipXY, Rotate270FlipY, Rotate90FlipNone, Rotate90FlipX, Rotate90FlipXY,             Rotate90FlipY, RotateNoneFlipNone, RotateNoneFlipX, RotateNoneFlipXY, RotateNoneFlipY.             Default is RotateNoneFlipNone.) (optional)

            saveOtherFrames (bool): Include all other frames or just specified frame in response. (optional)

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'frameId', 'newWidth', 'newHeight', 'x', 'y', 'rectWidth', 'rectHeight', 'rotateFlipMethod', 'saveOtherFrames', 'outPath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetImageFrame" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/frames/{frameId}/?appSid={appSid}&amp;newWidth={newWidth}&amp;newHeight={newHeight}&amp;x={x}&amp;y={y}&amp;rectWidth={rectWidth}&amp;rectHeight={rectHeight}&amp;rotateFlipMethod={rotateFlipMethod}&amp;saveOtherFrames={saveOtherFrames}&amp;outPath={outPath}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'frameId' in allParams and allParams['frameId'] is not None:
            resourcePath = resourcePath.replace("{" + "frameId" + "}" , str(allParams['frameId']))
        else:
            resourcePath = re.sub("[&?]frameId.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newWidth' in allParams and allParams['newWidth'] is not None:
            resourcePath = resourcePath.replace("{" + "newWidth" + "}" , str(allParams['newWidth']))
        else:
            resourcePath = re.sub("[&?]newWidth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newHeight' in allParams and allParams['newHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "newHeight" + "}" , str(allParams['newHeight']))
        else:
            resourcePath = re.sub("[&?]newHeight.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'x' in allParams and allParams['x'] is not None:
            resourcePath = resourcePath.replace("{" + "x" + "}" , str(allParams['x']))
        else:
            resourcePath = re.sub("[&?]x.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'y' in allParams and allParams['y'] is not None:
            resourcePath = resourcePath.replace("{" + "y" + "}" , str(allParams['y']))
        else:
            resourcePath = re.sub("[&?]y.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectWidth' in allParams and allParams['rectWidth'] is not None:
            resourcePath = resourcePath.replace("{" + "rectWidth" + "}" , str(allParams['rectWidth']))
        else:
            resourcePath = re.sub("[&?]rectWidth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectHeight' in allParams and allParams['rectHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "rectHeight" + "}" , str(allParams['rectHeight']))
        else:
            resourcePath = re.sub("[&?]rectHeight.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rotateFlipMethod' in allParams and allParams['rotateFlipMethod'] is not None:
            resourcePath = resourcePath.replace("{" + "rotateFlipMethod" + "}" , str(allParams['rotateFlipMethod']))
        else:
            resourcePath = re.sub("[&?]rotateFlipMethod.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'saveOtherFrames' in allParams and allParams['saveOtherFrames'] is not None:
            resourcePath = resourcePath.replace("{" + "saveOtherFrames" + "}" , str(allParams['saveOtherFrames']))
        else:
            resourcePath = re.sub("[&?]saveOtherFrames.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetImageFrameProperties(self, name, frameId, **kwargs):
        """Get properties of a tiff frame.
        Args:
            name (str): Filename with image. (required)

            frameId (int): Number of frame. (required)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ImagingResponse
        """

        allParams = dict.fromkeys(['name', 'frameId', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetImageFrameProperties" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/frames/{frameId}/properties/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'frameId' in allParams and allParams['frameId'] is not None:
            resourcePath = resourcePath.replace("{" + "frameId" + "}" , str(allParams['frameId']))
        else:
            resourcePath = re.sub("[&?]frameId.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ImagingResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetImageGif(self, name, **kwargs):
        """Update parameters of bmp image.
        Args:
            name (str): Filename of image. (required)

            backgroundColorIndex (int): Index of the background color. (optional)

            colorResolution (int): Color resolution. (optional)

            hasTrailer (bool): Specifies if image has trailer. (optional)

            interlaced (bool): Specifies if image is interlaced. (optional)

            isPaletteSorted (bool): Specifies if palette is sorted. (optional)

            pixelAspectRatio (int): Pixel aspect ratio. (optional)

            fromScratch (bool): Specifies where additional parameters we do not support should be taken from. If this is true

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'backgroundColorIndex', 'colorResolution', 'hasTrailer', 'interlaced', 'isPaletteSorted', 'pixelAspectRatio', 'fromScratch', 'outPath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetImageGif" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/gif/?appSid={appSid}&amp;backgroundColorIndex={backgroundColorIndex}&amp;colorResolution={colorResolution}&amp;hasTrailer={hasTrailer}&amp;interlaced={interlaced}&amp;isPaletteSorted={isPaletteSorted}&amp;pixelAspectRatio={pixelAspectRatio}&amp;fromScratch={fromScratch}&amp;outPath={outPath}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'backgroundColorIndex' in allParams and allParams['backgroundColorIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "backgroundColorIndex" + "}" , str(allParams['backgroundColorIndex']))
        else:
            resourcePath = re.sub("[&?]backgroundColorIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'colorResolution' in allParams and allParams['colorResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "colorResolution" + "}" , str(allParams['colorResolution']))
        else:
            resourcePath = re.sub("[&?]colorResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'hasTrailer' in allParams and allParams['hasTrailer'] is not None:
            resourcePath = resourcePath.replace("{" + "hasTrailer" + "}" , str(allParams['hasTrailer']))
        else:
            resourcePath = re.sub("[&?]hasTrailer.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'interlaced' in allParams and allParams['interlaced'] is not None:
            resourcePath = resourcePath.replace("{" + "interlaced" + "}" , str(allParams['interlaced']))
        else:
            resourcePath = re.sub("[&?]interlaced.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'isPaletteSorted' in allParams and allParams['isPaletteSorted'] is not None:
            resourcePath = resourcePath.replace("{" + "isPaletteSorted" + "}" , str(allParams['isPaletteSorted']))
        else:
            resourcePath = re.sub("[&?]isPaletteSorted.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pixelAspectRatio' in allParams and allParams['pixelAspectRatio'] is not None:
            resourcePath = resourcePath.replace("{" + "pixelAspectRatio" + "}" , str(allParams['pixelAspectRatio']))
        else:
            resourcePath = re.sub("[&?]pixelAspectRatio.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fromScratch' in allParams and allParams['fromScratch'] is not None:
            resourcePath = resourcePath.replace("{" + "fromScratch" + "}" , str(allParams['fromScratch']))
        else:
            resourcePath = re.sub("[&?]fromScratch.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostImageGif(self, file, **kwargs):
        """Update parameters of gif image.
        Args:
            backgroundColorIndex (int): Index of the background color. (optional)

            colorResolution (int): Color resolution. (optional)

            hasTrailer (bool): Specifies if image has trailer. (optional)

            interlaced (bool): Specifies if image is interlaced. (optional)

            isPaletteSorted (bool): Specifies if palette is sorted. (optional)

            pixelAspectRatio (int): Pixel aspect ratio. (optional)

            fromScratch (bool): Specifies where additional parameters we do not support should be taken from. If this is true

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['backgroundColorIndex', 'colorResolution', 'hasTrailer', 'interlaced', 'isPaletteSorted', 'pixelAspectRatio', 'fromScratch', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostImageBmp_ImagingApi_0" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/gif/?appSid={appSid}&amp;backgroundColorIndex={backgroundColorIndex}&amp;colorResolution={colorResolution}&amp;hasTrailer={hasTrailer}&amp;interlaced={interlaced}&amp;isPaletteSorted={isPaletteSorted}&amp;pixelAspectRatio={pixelAspectRatio}&amp;fromScratch={fromScratch}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'backgroundColorIndex' in allParams and allParams['backgroundColorIndex'] is not None:
            resourcePath = resourcePath.replace("{" + "backgroundColorIndex" + "}" , str(allParams['backgroundColorIndex']))
        else:
            resourcePath = re.sub("[&?]backgroundColorIndex.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'colorResolution' in allParams and allParams['colorResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "colorResolution" + "}" , str(allParams['colorResolution']))
        else:
            resourcePath = re.sub("[&?]colorResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'hasTrailer' in allParams and allParams['hasTrailer'] is not None:
            resourcePath = resourcePath.replace("{" + "hasTrailer" + "}" , str(allParams['hasTrailer']))
        else:
            resourcePath = re.sub("[&?]hasTrailer.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'interlaced' in allParams and allParams['interlaced'] is not None:
            resourcePath = resourcePath.replace("{" + "interlaced" + "}" , str(allParams['interlaced']))
        else:
            resourcePath = re.sub("[&?]interlaced.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'isPaletteSorted' in allParams and allParams['isPaletteSorted'] is not None:
            resourcePath = resourcePath.replace("{" + "isPaletteSorted" + "}" , str(allParams['isPaletteSorted']))
        else:
            resourcePath = re.sub("[&?]isPaletteSorted.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'pixelAspectRatio' in allParams and allParams['pixelAspectRatio'] is not None:
            resourcePath = resourcePath.replace("{" + "pixelAspectRatio" + "}" , str(allParams['pixelAspectRatio']))
        else:
            resourcePath = re.sub("[&?]pixelAspectRatio.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fromScratch' in allParams and allParams['fromScratch'] is not None:
            resourcePath = resourcePath.replace("{" + "fromScratch" + "}" , str(allParams['fromScratch']))
        else:
            resourcePath = re.sub("[&?]fromScratch.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetImageJpg(self, name, **kwargs):
        """Update parameters of jpg image.
        Args:
            name (str): Filename of image. (required)

            quality (int): Quality of image. From 0 to 100. Default is 75 (optional)

            compressionType (str): Compression type. (optional)

            fromScratch (bool): Specifies where additional parameters we do not support should be taken from. If this is true

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'quality', 'compressionType', 'fromScratch', 'outPath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetImageJpg" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/jpg/?appSid={appSid}&amp;quality={quality}&amp;compressionType={compressionType}&amp;fromScratch={fromScratch}&amp;outPath={outPath}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'quality' in allParams and allParams['quality'] is not None:
            resourcePath = resourcePath.replace("{" + "quality" + "}" , str(allParams['quality']))
        else:
            resourcePath = re.sub("[&?]quality.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'compressionType' in allParams and allParams['compressionType'] is not None:
            resourcePath = resourcePath.replace("{" + "compressionType" + "}" , str(allParams['compressionType']))
        else:
            resourcePath = re.sub("[&?]compressionType.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fromScratch' in allParams and allParams['fromScratch'] is not None:
            resourcePath = resourcePath.replace("{" + "fromScratch" + "}" , str(allParams['fromScratch']))
        else:
            resourcePath = re.sub("[&?]fromScratch.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostImageJpg(self, file, **kwargs):
        """Update parameters of jpg image.
        Args:
            quality (int): Quality of image. From 0 to 100. Default is 75 (optional)

            compressionType (str): Compression type. (optional)

            fromScratch (bool): Specifies where additional parameters we do not support should be taken from. If this is true

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['quality', 'compressionType', 'fromScratch', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostImageJpg" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/jpg/?appSid={appSid}&amp;quality={quality}&amp;compressionType={compressionType}&amp;fromScratch={fromScratch}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'quality' in allParams and allParams['quality'] is not None:
            resourcePath = resourcePath.replace("{" + "quality" + "}" , str(allParams['quality']))
        else:
            resourcePath = re.sub("[&?]quality.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'compressionType' in allParams and allParams['compressionType'] is not None:
            resourcePath = resourcePath.replace("{" + "compressionType" + "}" , str(allParams['compressionType']))
        else:
            resourcePath = re.sub("[&?]compressionType.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fromScratch' in allParams and allParams['fromScratch'] is not None:
            resourcePath = resourcePath.replace("{" + "fromScratch" + "}" , str(allParams['fromScratch']))
        else:
            resourcePath = re.sub("[&?]fromScratch.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetImagePng(self, name, **kwargs):
        """Update parameters of png image.
        Args:
            name (str): Filename of image. (required)

            fromScratch (bool): Specifies where additional parameters we do not support should be taken from. If this is true

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'fromScratch', 'outPath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetImagePng" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/png/?appSid={appSid}&amp;fromScratch={fromScratch}&amp;outPath={outPath}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fromScratch' in allParams and allParams['fromScratch'] is not None:
            resourcePath = resourcePath.replace("{" + "fromScratch" + "}" , str(allParams['fromScratch']))
        else:
            resourcePath = re.sub("[&?]fromScratch.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostImagePng(self, file, **kwargs):
        """Update parameters of png image.
        Args:
            fromScratch (bool): Specifies where additional parameters we do not support should be taken from. If this is true

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['fromScratch', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostImagePng" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/png/?appSid={appSid}&amp;fromScratch={fromScratch}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'fromScratch' in allParams and allParams['fromScratch'] is not None:
            resourcePath = resourcePath.replace("{" + "fromScratch" + "}" , str(allParams['fromScratch']))
        else:
            resourcePath = re.sub("[&?]fromScratch.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetImageProperties(self, name, **kwargs):
        """Get properties of an image.
        Args:
            name (str): The image name. (required)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ImagingResponse
        """

        allParams = dict.fromkeys(['name', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetImageProperties" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/properties/?appSid={appSid}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ImagingResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetImagePsd(self, name, **kwargs):
        """Update parameters of psd image.
        Args:
            name (str): Filename of image. (required)

            channelsCount (int): Count of channels. (optional)

            compressionMethod (str): Compression method. (optional)

            fromScratch (bool): Specifies where additional parameters we do not support should be taken from. If this is true

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'channelsCount', 'compressionMethod', 'fromScratch', 'outPath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetImagePsd" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/psd/?appSid={appSid}&amp;channelsCount={channelsCount}&amp;compressionMethod={compressionMethod}&amp;fromScratch={fromScratch}&amp;outPath={outPath}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'channelsCount' in allParams and allParams['channelsCount'] is not None:
            resourcePath = resourcePath.replace("{" + "channelsCount" + "}" , str(allParams['channelsCount']))
        else:
            resourcePath = re.sub("[&?]channelsCount.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'compressionMethod' in allParams and allParams['compressionMethod'] is not None:
            resourcePath = resourcePath.replace("{" + "compressionMethod" + "}" , str(allParams['compressionMethod']))
        else:
            resourcePath = re.sub("[&?]compressionMethod.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fromScratch' in allParams and allParams['fromScratch'] is not None:
            resourcePath = resourcePath.replace("{" + "fromScratch" + "}" , str(allParams['fromScratch']))
        else:
            resourcePath = re.sub("[&?]fromScratch.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostImagePsd(self, file, **kwargs):
        """Update parameters of psd image.
        Args:
            channelsCount (int): Count of channels. (optional)

            compressionMethod (str): Compression method. (optional)

            fromScratch (bool): Specifies where additional parameters we do not support should be taken from. If this is true

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['channelsCount', 'compressionMethod', 'fromScratch', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostImagePsd" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/psd/?appSid={appSid}&amp;channelsCount={channelsCount}&amp;compressionMethod={compressionMethod}&amp;fromScratch={fromScratch}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'channelsCount' in allParams and allParams['channelsCount'] is not None:
            resourcePath = resourcePath.replace("{" + "channelsCount" + "}" , str(allParams['channelsCount']))
        else:
            resourcePath = re.sub("[&?]channelsCount.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'compressionMethod' in allParams and allParams['compressionMethod'] is not None:
            resourcePath = resourcePath.replace("{" + "compressionMethod" + "}" , str(allParams['compressionMethod']))
        else:
            resourcePath = re.sub("[&?]compressionMethod.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fromScratch' in allParams and allParams['fromScratch'] is not None:
            resourcePath = resourcePath.replace("{" + "fromScratch" + "}" , str(allParams['fromScratch']))
        else:
            resourcePath = re.sub("[&?]fromScratch.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetChangeImageScale(self, name, format, newWidth, newHeight, **kwargs):
        """Change scale of an existing image
        Args:
            name (str): The image name. (required)

            format (str): Output file format. Valid Formats: Bmp, png, jpg, tiff, psd, gif. (required)

            newWidth (int): New width of the scaled image. (required)

            newHeight (int): New height of the scaled image. (required)

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'format', 'newWidth', 'newHeight', 'outPath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetChangeImageScale" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/resize/?appSid={appSid}&amp;toFormat={toFormat}&amp;newWidth={newWidth}&amp;newHeight={newHeight}&amp;outPath={outPath}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newWidth' in allParams and allParams['newWidth'] is not None:
            resourcePath = resourcePath.replace("{" + "newWidth" + "}" , str(allParams['newWidth']))
        else:
            resourcePath = re.sub("[&?]newWidth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newHeight' in allParams and allParams['newHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "newHeight" + "}" , str(allParams['newHeight']))
        else:
            resourcePath = re.sub("[&?]newHeight.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostChangeImageScale(self, format, newWidth, newHeight, file, **kwargs):
        """Change scale of an image from body
        Args:
            format (str): Output file format. Valid Formats: Bmp, png, jpg, tiff, psd, gif. (required)

            newWidth (int): New width of the scaled image. (required)

            newHeight (int): New height of the scaled image. (required)

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['format', 'newWidth', 'newHeight', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostChangeImageScale" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/resize/?appSid={appSid}&amp;toFormat={toFormat}&amp;newWidth={newWidth}&amp;newHeight={newHeight}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newWidth' in allParams and allParams['newWidth'] is not None:
            resourcePath = resourcePath.replace("{" + "newWidth" + "}" , str(allParams['newWidth']))
        else:
            resourcePath = re.sub("[&?]newWidth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newHeight' in allParams and allParams['newHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "newHeight" + "}" , str(allParams['newHeight']))
        else:
            resourcePath = re.sub("[&?]newHeight.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetImageRotateFlip(self, name, format, method, **kwargs):
        """Rotate and flip existing image
        Args:
            name (str): Filename of image. (required)

            format (str): Number of frame. (Bmp, png, jpg, tiff, psd, gif.) (required)

            method (str): New width of the scaled image. (Rotate180FlipNone,  Rotate180FlipX, Rotate180FlipXY, Rotate180FlipY, Rotate270FlipNone, Rotate270FlipX, Rotate270FlipXY, Rotate270FlipY, Rotate90FlipNone, Rotate90FlipX, Rotate90FlipXY, Rotate90FlipY, RotateNoneFlipNone, RotateNoneFlipX, RotateNoneFlipXY, RotateNoneFlipY) (required)

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'format', 'method', 'outPath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetImageRotateFlip" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/rotateflip/?toFormat={toFormat}&amp;appSid={appSid}&amp;method={method}&amp;outPath={outPath}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'method' in allParams and allParams['method'] is not None:
            resourcePath = resourcePath.replace("{" + "method" + "}" , str(allParams['method']))
        else:
            resourcePath = re.sub("[&?]method.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostImageRotateFlip(self, format, method, file, **kwargs):
        """Rotate and flip existing image and get it from response.
        Args:
            format (str): Number of frame. (Bmp, png, jpg, tiff, psd, gif.) (required)

            method (str): New width of the scaled image. (Rotate180FlipNone,  Rotate180FlipX, Rotate180FlipXY, Rotate180FlipY, Rotate270FlipNone, Rotate270FlipX, Rotate270FlipXY, Rotate270FlipY, Rotate90FlipNone, Rotate90FlipX, Rotate90FlipXY, Rotate90FlipY, RotateNoneFlipNone, RotateNoneFlipX, RotateNoneFlipXY, RotateNoneFlipY) (required)

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['format', 'method', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostImageRotateFlip" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/rotateflip/?toFormat={toFormat}&amp;appSid={appSid}&amp;method={method}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'method' in allParams and allParams['method'] is not None:
            resourcePath = resourcePath.replace("{" + "method" + "}" , str(allParams['method']))
        else:
            resourcePath = re.sub("[&?]method.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetImageSaveAs(self, name, format, **kwargs):
        """Export existing image to another format
        Args:
            name (str): Filename of image. (required)

            format (str): Output file format. (Bmp, png, jpg, tiff, psd, gif.) (required)

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'format', 'outPath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetImageSaveAs" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/saveAs/?appSid={appSid}&amp;toFormat={toFormat}&amp;outPath={outPath}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostImageSaveAs(self, format, file, **kwargs):
        """Export existing image to another format. Image is passed as request body.
        Args:
            format (str): Output file format. (Bmp, png, jpg, tiff, psd, gif.) (required)

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['format', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostImageSaveAs" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/saveAs/?appSid={appSid}&amp;toFormat={toFormat}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetTiffToFax(self, name, **kwargs):
        """Get tiff image for fax.
        Args:
            name (str): The image file name. (required)

            storage (str): The image file storage. (optional)

            folder (str): The image file folder. (optional)

            outPath (str): Path to save result (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder', 'outPath'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetTiffToFax" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/tiff/{name}/toFax/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostProcessTiff(self, file, **kwargs):
        """Update tiff image.
        Args:
            compression (str): New compression. (optional)

            resolutionUnit (str): New resolution unit. (optional)

            bitDepth (int): New bit depth. (optional)

            fromScratch (bool):  (optional)

            horizontalResolution (float): New horizontal resolution. (optional)

            verticalResolution (float): New verstical resolution. (optional)

            outPath (str): Path to save result (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['compression', 'resolutionUnit', 'bitDepth', 'fromScratch', 'horizontalResolution', 'verticalResolution', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostProcessTiff" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/tiff/?appSid={appSid}&amp;compression={compression}&amp;resolutionUnit={resolutionUnit}&amp;bitDepth={bitDepth}&amp;fromScratch={fromScratch}&amp;horizontalResolution={horizontalResolution}&amp;verticalResolution={verticalResolution}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'compression' in allParams and allParams['compression'] is not None:
            resourcePath = resourcePath.replace("{" + "compression" + "}" , str(allParams['compression']))
        else:
            resourcePath = re.sub("[&?]compression.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'resolutionUnit' in allParams and allParams['resolutionUnit'] is not None:
            resourcePath = resourcePath.replace("{" + "resolutionUnit" + "}" , str(allParams['resolutionUnit']))
        else:
            resourcePath = re.sub("[&?]resolutionUnit.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'bitDepth' in allParams and allParams['bitDepth'] is not None:
            resourcePath = resourcePath.replace("{" + "bitDepth" + "}" , str(allParams['bitDepth']))
        else:
            resourcePath = re.sub("[&?]bitDepth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fromScratch' in allParams and allParams['fromScratch'] is not None:
            resourcePath = resourcePath.replace("{" + "fromScratch" + "}" , str(allParams['fromScratch']))
        else:
            resourcePath = re.sub("[&?]fromScratch.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'horizontalResolution' in allParams and allParams['horizontalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "horizontalResolution" + "}" , str(allParams['horizontalResolution']))
        else:
            resourcePath = re.sub("[&?]horizontalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'verticalResolution' in allParams and allParams['verticalResolution'] is not None:
            resourcePath = resourcePath.replace("{" + "verticalResolution" + "}" , str(allParams['verticalResolution']))
        else:
            resourcePath = re.sub("[&?]verticalResolution.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostTiffAppend(self, name, **kwargs):
        """Append tiff image.
        Args:
            name (str): Original image name. (required)

            appendFile (str): Second image file name. (optional)

            storage (str): The images storage. (optional)

            folder (str): The images folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'appendFile', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostTiffAppend" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/tiff/{name}/appendTiff/?appSid={appSid}&amp;appendFile={appendFile}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'appendFile' in allParams and allParams['appendFile'] is not None:
            resourcePath = resourcePath.replace("{" + "appendFile" + "}" , str(allParams['appendFile']))
        else:
            resourcePath = re.sub("[&?]appendFile.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'SaaSposeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetUpdatedImage(self, name, format, newWidth, newHeight, x, y, rectWidth, rectHeight, rotateFlipMethod, **kwargs):
        """Perform scaling, cropping and flipping of an image in single request.
        Args:
            name (str): Filename of image. (required)

            format (str): Save image in another format. By default format remains the same (required)

            newWidth (int): New Width of the scaled image. (required)

            newHeight (int): New height of the scaled image. (required)

            x (int): X position of start point for cropping rectangle (required)

            y (int): Y position of start point for cropping rectangle (required)

            rectWidth (int): Width of cropping rectangle (required)

            rectHeight (int): Height of cropping rectangle (required)

            rotateFlipMethod (str): RotateFlip method. Default is RotateNoneFlipNone. (required)

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            folder (str): Folder with image to process. (optional)

            storage (str):  (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'format', 'newWidth', 'newHeight', 'x', 'y', 'rectWidth', 'rectHeight', 'rotateFlipMethod', 'outPath', 'folder', 'storage'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetUpdatedImage" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/{name}/updateImage/?appSid={appSid}&amp;toFormat={toFormat}&amp;newWidth={newWidth}&amp;newHeight={newHeight}&amp;x={x}&amp;y={y}&amp;rectWidth={rectWidth}&amp;rectHeight={rectHeight}&amp;rotateFlipMethod={rotateFlipMethod}&amp;outPath={outPath}&amp;folder={folder}&amp;storage={storage}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newWidth' in allParams and allParams['newWidth'] is not None:
            resourcePath = resourcePath.replace("{" + "newWidth" + "}" , str(allParams['newWidth']))
        else:
            resourcePath = re.sub("[&?]newWidth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newHeight' in allParams and allParams['newHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "newHeight" + "}" , str(allParams['newHeight']))
        else:
            resourcePath = re.sub("[&?]newHeight.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'x' in allParams and allParams['x'] is not None:
            resourcePath = resourcePath.replace("{" + "x" + "}" , str(allParams['x']))
        else:
            resourcePath = re.sub("[&?]x.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'y' in allParams and allParams['y'] is not None:
            resourcePath = resourcePath.replace("{" + "y" + "}" , str(allParams['y']))
        else:
            resourcePath = re.sub("[&?]y.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectWidth' in allParams and allParams['rectWidth'] is not None:
            resourcePath = resourcePath.replace("{" + "rectWidth" + "}" , str(allParams['rectWidth']))
        else:
            resourcePath = re.sub("[&?]rectWidth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectHeight' in allParams and allParams['rectHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "rectHeight" + "}" , str(allParams['rectHeight']))
        else:
            resourcePath = re.sub("[&?]rectHeight.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rotateFlipMethod' in allParams and allParams['rotateFlipMethod'] is not None:
            resourcePath = resourcePath.replace("{" + "rotateFlipMethod" + "}" , str(allParams['rotateFlipMethod']))
        else:
            resourcePath = re.sub("[&?]rotateFlipMethod.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostImageSaveAs_ImagingApi_0(self, format, newWidth, newHeight, x, y, rectWidth, rectHeight, rotateFlipMethod, file, **kwargs):
        """Perform scaling, cropping and flipping of an image in single request. Image is passed as request body.
        Args:
            format (str): Save image in another format. By default format remains the same (required)

            newWidth (int): New Width of the scaled image. (required)

            newHeight (int): New height of the scaled image. (required)

            x (int): X position of start point for cropping rectangle (required)

            y (int): Y position of start point for cropping rectangle (required)

            rectWidth (int): Width of cropping rectangle (required)

            rectHeight (int): Height of cropping rectangle (required)

            rotateFlipMethod (str): RotateFlip method. Default is RotateNoneFlipNone. (required)

            outPath (str): Path to updated file, if this is empty, response contains streamed image. (optional)

            file (File):  (required)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['format', 'newWidth', 'newHeight', 'x', 'y', 'rectWidth', 'rectHeight', 'rotateFlipMethod', 'outPath', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostImageSaveAs_ImagingApi_0" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/imaging/updateImage/?appSid={appSid}&amp;toFormat={toFormat}&amp;newWidth={newWidth}&amp;newHeight={newHeight}&amp;x={x}&amp;y={y}&amp;rectWidth={rectWidth}&amp;rectHeight={rectHeight}&amp;rotateFlipMethod={rotateFlipMethod}&amp;outPath={outPath}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newWidth' in allParams and allParams['newWidth'] is not None:
            resourcePath = resourcePath.replace("{" + "newWidth" + "}" , str(allParams['newWidth']))
        else:
            resourcePath = re.sub("[&?]newWidth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'newHeight' in allParams and allParams['newHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "newHeight" + "}" , str(allParams['newHeight']))
        else:
            resourcePath = re.sub("[&?]newHeight.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'x' in allParams and allParams['x'] is not None:
            resourcePath = resourcePath.replace("{" + "x" + "}" , str(allParams['x']))
        else:
            resourcePath = re.sub("[&?]x.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'y' in allParams and allParams['y'] is not None:
            resourcePath = resourcePath.replace("{" + "y" + "}" , str(allParams['y']))
        else:
            resourcePath = re.sub("[&?]y.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectWidth' in allParams and allParams['rectWidth'] is not None:
            resourcePath = resourcePath.replace("{" + "rectWidth" + "}" , str(allParams['rectWidth']))
        else:
            resourcePath = re.sub("[&?]rectWidth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectHeight' in allParams and allParams['rectHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "rectHeight" + "}" , str(allParams['rectHeight']))
        else:
            resourcePath = re.sub("[&?]rectHeight.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rotateFlipMethod' in allParams and allParams['rotateFlipMethod'] is not None:
            resourcePath = resourcePath.replace("{" + "rotateFlipMethod" + "}" , str(allParams['rotateFlipMethod']))
        else:
            resourcePath = re.sub("[&?]rotateFlipMethod.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'outPath' in allParams and allParams['outPath'] is not None:
            resourcePath = resourcePath.replace("{" + "outPath" + "}" , str(allParams['outPath']))
        else:
            resourcePath = re.sub("[&?]outPath.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { 'file':open(file, 'rb')}
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/octet-stream'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResponseMessage', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    




