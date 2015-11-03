#!/usr/bin/env python

import sys
import os
import urllib
import json
import re
from models import *
from ApiClient import ApiException


class OcrApi(object):

    def __init__(self, apiClient):
      self.apiClient = apiClient

    

    def GetRecognizeDocument(self, name, **kwargs):
        """Recognize image text, language and text region can be selected, default dictionaries can be used for correction.
        Args:
            name (str): Name of the file to recognize. (required)

            language (str): Language of the document. (optional)

            rectX (int): Top left point X coordinate of  to recognize text inside. (optional)

            rectY (int): Top left point Y coordinate of  to recognize text inside. (optional)

            rectWidth (int): Width of  to recognize text inside. (optional)

            rectHeight (int): Height of  to recognize text inside. (optional)

            useDefaultDictionaries (bool): Use default dictionaries for result correction. (optional)

            storage (str): Image's storage. (optional)

            folder (str): Image's folder. (optional)

            

        Returns: OCRResponse
        """

        allParams = dict.fromkeys(['name', 'language', 'rectX', 'rectY', 'rectWidth', 'rectHeight', 'useDefaultDictionaries', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetRecognizeDocument" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/ocr/{name}/recognize/?appSid={appSid}&amp;language={language}&amp;rectX={rectX}&amp;rectY={rectY}&amp;rectWidth={rectWidth}&amp;rectHeight={rectHeight}&amp;useDefaultDictionaries={useDefaultDictionaries}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'language' in allParams and allParams['language'] is not None:
            resourcePath = resourcePath.replace("{" + "language" + "}" , str(allParams['language']))
        else:
            resourcePath = re.sub("[&?]language.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectX' in allParams and allParams['rectX'] is not None:
            resourcePath = resourcePath.replace("{" + "rectX" + "}" , str(allParams['rectX']))
        else:
            resourcePath = re.sub("[&?]rectX.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectY' in allParams and allParams['rectY'] is not None:
            resourcePath = resourcePath.replace("{" + "rectY" + "}" , str(allParams['rectY']))
        else:
            resourcePath = re.sub("[&?]rectY.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectWidth' in allParams and allParams['rectWidth'] is not None:
            resourcePath = resourcePath.replace("{" + "rectWidth" + "}" , str(allParams['rectWidth']))
        else:
            resourcePath = re.sub("[&?]rectWidth.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'rectHeight' in allParams and allParams['rectHeight'] is not None:
            resourcePath = resourcePath.replace("{" + "rectHeight" + "}" , str(allParams['rectHeight']))
        else:
            resourcePath = re.sub("[&?]rectHeight.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'useDefaultDictionaries' in allParams and allParams['useDefaultDictionaries'] is not None:
            resourcePath = resourcePath.replace("{" + "useDefaultDictionaries" + "}" , str(allParams['useDefaultDictionaries']))
        else:
            resourcePath = re.sub("[&?]useDefaultDictionaries.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'OCRResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostOcrFromUrlOrContent(self, file, **kwargs):
        """Recognize image text from some url if provided or from the request body content, language can be selected, default dictionaries can be used for correction.
        Args:
            url (str): The image file url. (optional)

            language (str): Language of the document. (optional)

            useDefaultDictionaries (bool): Use default dictionaries for result correction. (optional)

            file (File):  (required)

            

        Returns: OCRResponse
        """

        allParams = dict.fromkeys(['url', 'language', 'useDefaultDictionaries', 'file'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostOcrFromUrlOrContent" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/ocr/recognize/?appSid={appSid}&amp;url={url}&amp;language={language}&amp;useDefaultDictionaries={useDefaultDictionaries}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'url' in allParams and allParams['url'] is not None:
            resourcePath = resourcePath.replace("{" + "url" + "}" , str(allParams['url']))
        else:
            resourcePath = re.sub("[&?]url.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'language' in allParams and allParams['language'] is not None:
            resourcePath = resourcePath.replace("{" + "language" + "}" , str(allParams['language']))
        else:
            resourcePath = re.sub("[&?]language.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'useDefaultDictionaries' in allParams and allParams['useDefaultDictionaries'] is not None:
            resourcePath = resourcePath.replace("{" + "useDefaultDictionaries" + "}" , str(allParams['useDefaultDictionaries']))
        else:
            resourcePath = re.sub("[&?]useDefaultDictionaries.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = {}
        
        if file is not None:
            files = { 'file':open(file, 'rb')}
            
        bodyParam = None

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'multipart/form-data'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'OCRResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    




