#!/usr/bin/env python

import sys
import os
import urllib
import json
import re
from models import *
from ApiClient import ApiException


class TasksApi(object):

    def __init__(self, apiClient):
      self.apiClient = apiClient

    

    def DeleteProjectAssignment(self, name, assignmentUid, **kwargs):
        """Deletes a project assignment with all references to it.
        Args:
            name (str): The name of the file. (required)

            assignmentUid (int): assignment Uid (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'assignmentUid', 'storage', 'folder', 'fileName'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteProjectAssignment" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/assignments/{assignmentUid}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}&amp;fileName={fileName}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'assignmentUid' in allParams and allParams['assignmentUid'] is not None:
            resourcePath = resourcePath.replace("{" + "assignmentUid" + "}" , str(allParams['assignmentUid']))
        else:
            resourcePath = re.sub("[&?]assignmentUid.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
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

        

        

    def GetProjectAssignment(self, name, assignmentUid, **kwargs):
        """Read project assignment.
        Args:
            name (str): The name of the file. (required)

            assignmentUid (int): Assignment Uid (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: AssignmentResponse
        """

        allParams = dict.fromkeys(['name', 'assignmentUid', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetProjectAssignment" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/assignments/{assignmentUid}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'assignmentUid' in allParams and allParams['assignmentUid'] is not None:
            resourcePath = resourcePath.replace("{" + "assignmentUid" + "}" , str(allParams['assignmentUid']))
        else:
            resourcePath = re.sub("[&?]assignmentUid.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'AssignmentResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetProjectAssignments(self, name, **kwargs):
        """Read project assignment items.
        Args:
            name (str): The name of the file. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: AssignmentItemsResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetProjectAssignments" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/assignments/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'AssignmentItemsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostProjectAssignment(self, name, taskUid, resourceUid, **kwargs):
        """Adds a new assignment to a project and returns assignment item in a response.
        Args:
            name (str): The name of the file. (required)

            taskUid (int): The unique id of the task to be assigned. (required)

            resourceUid (int): The unique id of the resource to be assigned. (required)

            units (float): The units for the new assignment. Default value is 1. (optional)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: AssignmentItemResponse
        """

        allParams = dict.fromkeys(['name', 'taskUid', 'resourceUid', 'units', 'fileName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostProjectAssignment" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/assignments/?appSid={appSid}&amp;taskUid={taskUid}&amp;resourceUid={resourceUid}&amp;units={units}&amp;fileName={fileName}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'taskUid' in allParams and allParams['taskUid'] is not None:
            resourcePath = resourcePath.replace("{" + "taskUid" + "}" , str(allParams['taskUid']))
        else:
            resourcePath = re.sub("[&?]taskUid.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'resourceUid' in allParams and allParams['resourceUid'] is not None:
            resourcePath = resourcePath.replace("{" + "resourceUid" + "}" , str(allParams['resourceUid']))
        else:
            resourcePath = re.sub("[&?]resourceUid.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'units' in allParams and allParams['units'] is not None:
            resourcePath = resourcePath.replace("{" + "units" + "}" , str(allParams['units']))
        else:
            resourcePath = re.sub("[&?]units.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'AssignmentItemResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteCalendarException(self, name, calendarUid, index, **kwargs):
        """Deletes calendar exception from calendar exceptions collection.
        Args:
            name (str): The name of the file. (required)

            calendarUid (int): Calendar Uid (required)

            index (int): Calendar exception index (required)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'calendarUid', 'index', 'fileName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteCalendarException" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/calendars/{calendarUid}/calendarExceptions/{index}/?appSid={appSid}&amp;fileName={fileName}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'calendarUid' in allParams and allParams['calendarUid'] is not None:
            resourcePath = resourcePath.replace("{" + "calendarUid" + "}" , str(allParams['calendarUid']))
        else:
            resourcePath = re.sub("[&?]calendarUid.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'index' in allParams and allParams['index'] is not None:
            resourcePath = resourcePath.replace("{" + "index" + "}" , str(allParams['index']))
        else:
            resourcePath = re.sub("[&?]index.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
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

        

        

    def DeleteProjectCalendar(self, name, calendarUid, **kwargs):
        """Deletes a project calendar
        Args:
            name (str): The name of the file. (required)

            calendarUid (int): Calendar Uid (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'calendarUid', 'storage', 'folder', 'fileName'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteProjectCalendar" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/calendars/{calendarUid}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}&amp;fileName={fileName}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'calendarUid' in allParams and allParams['calendarUid'] is not None:
            resourcePath = resourcePath.replace("{" + "calendarUid" + "}" , str(allParams['calendarUid']))
        else:
            resourcePath = re.sub("[&?]calendarUid.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
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

        

        

    def GetCalendarExceptions(self, name, calendarUid, **kwargs):
        """Get list of calendar exceptions.
        Args:
            name (str): The name of the file. (required)

            calendarUid (int): Calendar Uid (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: CalendarExceptionsResponse
        """

        allParams = dict.fromkeys(['name', 'calendarUid', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetCalendarExceptions" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/calendars/{calendarUid}/calendarExceptions/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'calendarUid' in allParams and allParams['calendarUid'] is not None:
            resourcePath = resourcePath.replace("{" + "calendarUid" + "}" , str(allParams['calendarUid']))
        else:
            resourcePath = re.sub("[&?]calendarUid.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'CalendarExceptionsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetProjectCalendar(self, name, calendarUid, **kwargs):
        """Represents a project calendar.
        Args:
            name (str): The name of the file. (required)

            calendarUid (int): Calendar Uid (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: CalendarResponse
        """

        allParams = dict.fromkeys(['name', 'calendarUid', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetProjectCalendar" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/calendars/{calendarUid}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'calendarUid' in allParams and allParams['calendarUid'] is not None:
            resourcePath = resourcePath.replace("{" + "calendarUid" + "}" , str(allParams['calendarUid']))
        else:
            resourcePath = re.sub("[&?]calendarUid.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'CalendarResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetProjectCalendars(self, name, **kwargs):
        """Read project calendar items.
        Args:
            name (str): The name of the file. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: CalendarItemsResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetProjectCalendars" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/calendars/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'CalendarItemsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostCalendarExceptions(self, name, calendarUid, body, **kwargs):
        """Adds a new calendar exception to a calendar.
        Args:
            name (str): The name of the file. (required)

            calendarUid (int): Calendar Uid (required)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (CalendarException): CalendarException DTO (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'calendarUid', 'fileName', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostCalendarExceptions" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/calendars/{calendarUid}/calendarExceptions/?appSid={appSid}&amp;fileName={fileName}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'calendarUid' in allParams and allParams['calendarUid'] is not None:
            resourcePath = resourcePath.replace("{" + "calendarUid" + "}" , str(allParams['calendarUid']))
        else:
            resourcePath = re.sub("[&?]calendarUid.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

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
        bodyParam = body

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

        

        

    def PostProjectCalendar(self, name, body, **kwargs):
        """Adds a new calendar to project file.
        Args:
            name (str): The name of the file. (required)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (Calendar): Calendar DTO (required)

            

        Returns: CalendarItemResponse
        """

        allParams = dict.fromkeys(['name', 'fileName', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostProjectCalendar" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/calendars/?appSid={appSid}&amp;fileName={fileName}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

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
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'CalendarItemResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutCalendarException(self, name, calendarUid, index, body, **kwargs):
        """Updates calendar exception.
        Args:
            name (str): The name of the file. (required)

            calendarUid (int): Calendar Uid (required)

            index (int): Calendar exception index (required)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            body (CalendarException): CalendarException DTO (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'calendarUid', 'index', 'fileName', 'storage', 'folder', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutCalendarException" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/calendars/{calendarUid}/calendarExceptions/{index}/?appSid={appSid}&amp;fileName={fileName}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'calendarUid' in allParams and allParams['calendarUid'] is not None:
            resourcePath = resourcePath.replace("{" + "calendarUid" + "}" , str(allParams['calendarUid']))
        else:
            resourcePath = re.sub("[&?]calendarUid.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'index' in allParams and allParams['index'] is not None:
            resourcePath = resourcePath.replace("{" + "index" + "}" , str(allParams['index']))
        else:
            resourcePath = re.sub("[&?]index.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

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

        

        

    def GetCriticalPath(self, name, **kwargs):
        """Returns created report in PDF format.
        Args:
            name (str): The name of the file. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: TaskItemsResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetCriticalPath" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/criticalPath/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'TaskItemsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetTaskDocument(self, name, **kwargs):
        """Represents a project document.
        Args:
            name (str): The name of the file. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: DocumentResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetTaskDocument" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetTaskDocumentWithFormat(self, name, format, **kwargs):
        """Represents a project document with format
        Args:
            name (str): The name of the file. (required)

            format (str): The original format of the file. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'format', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetTaskDocumentWithFormat" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/?appSid={appSid}&amp;toFormat={toFormat}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'format' in allParams and allParams['format'] is not None:
            resourcePath = resourcePath.replace("{" + "format" + "}" , str(allParams['format']))
        else:
            resourcePath = re.sub("[&?]format.*?(?=&|\\?|$)", "", resourcePath)
        

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

        

        

    def GetDocumentProperties(self, name, **kwargs):
        """Read document properties.
        Args:
            name (str): The document name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: DocumentPropertiesResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetDocumentProperties" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/documentproperties/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentPropertiesResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetDocumentProperty(self, name, propertyName, **kwargs):
        """Read document property by name.
        Args:
            name (str): The document name. (required)

            propertyName (str): The property name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: DocumentPropertyResponse
        """

        allParams = dict.fromkeys(['name', 'propertyName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetDocumentProperty" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/documentproperties/{propertyName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'propertyName' in allParams and allParams['propertyName'] is not None:
            resourcePath = resourcePath.replace("{" + "propertyName" + "}" , str(allParams['propertyName']))
        else:
            resourcePath = re.sub("[&?]propertyName.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentPropertyResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostDocumentProperty(self, name, propertyName, body, **kwargs):
        """Set/create document property.
        Args:
            name (str): The document name. (required)

            propertyName (str): The property name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            filename (str): Name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            body (DocumentProperty): with new property value. (required)

            

        Returns: DocumentPropertyResponse
        """

        allParams = dict.fromkeys(['name', 'propertyName', 'storage', 'folder', 'filename', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostDocumentProperty" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/documentproperties/{propertyName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}&amp;filename={filename}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'propertyName' in allParams and allParams['propertyName'] is not None:
            resourcePath = resourcePath.replace("{" + "propertyName" + "}" , str(allParams['propertyName']))
        else:
            resourcePath = re.sub("[&?]propertyName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'filename' in allParams and allParams['filename'] is not None:
            resourcePath = resourcePath.replace("{" + "filename" + "}" , str(allParams['filename']))
        else:
            resourcePath = re.sub("[&?]filename.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentPropertyResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PutDocumentProperty(self, name, propertyName, body, **kwargs):
        """Set/create document property.
        Args:
            name (str): The document name. (required)

            propertyName (str): The property name. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            filename (str): Name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            body (DocumentProperty): with new property value. (required)

            

        Returns: DocumentPropertyResponse
        """

        allParams = dict.fromkeys(['name', 'propertyName', 'storage', 'folder', 'filename', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutDocumentProperty" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/documentproperties/{propertyName}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}&amp;filename={filename}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'propertyName' in allParams and allParams['propertyName'] is not None:
            resourcePath = resourcePath.replace("{" + "propertyName" + "}" , str(allParams['propertyName']))
        else:
            resourcePath = re.sub("[&?]propertyName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'filename' in allParams and allParams['filename'] is not None:
            resourcePath = resourcePath.replace("{" + "filename" + "}" , str(allParams['filename']))
        else:
            resourcePath = re.sub("[&?]filename.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'DocumentPropertyResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteExtendedAttributeByIndex(self, name, index, **kwargs):
        """Delete a project extended attribute.
        Args:
            name (str): The name of the file. (required)

            index (int): Index of extended attribute (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'index', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteExtendedAttributeByIndex" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/extendedAttributes/{index}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'index' in allParams and allParams['index'] is not None:
            resourcePath = resourcePath.replace("{" + "index" + "}" , str(allParams['index']))
        else:
            resourcePath = re.sub("[&?]index.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
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

        

        

    def GetExtendedAttributeByIndex(self, name, index, **kwargs):
        """Represents a project extended attribute definition.
        Args:
            name (str): The name of the file. (required)

            index (int): Index of extended attribute (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ExtendedAttributeResponse
        """

        allParams = dict.fromkeys(['name', 'index', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetExtendedAttributeByIndex" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/extendedAttributes/{index}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'index' in allParams and allParams['index'] is not None:
            resourcePath = resourcePath.replace("{" + "index" + "}" , str(allParams['index']))
        else:
            resourcePath = re.sub("[&?]index.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ExtendedAttributeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetExtendedAttributes(self, name, **kwargs):
        """Represents a project document.
        Args:
            name (str): The name of the file. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ExtendedAttributeItemsResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetExtendedAttributes" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/extendedAttributes/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ExtendedAttributeItemsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteOutlineCodeByIndex(self, name, index, **kwargs):
        """Deletes a project outline code
        Args:
            name (str): The name of the file. (required)

            index (int): Outline code index (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'index', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteOutlineCodeByIndex" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/outlineCodes/{index}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'index' in allParams and allParams['index'] is not None:
            resourcePath = resourcePath.replace("{" + "index" + "}" , str(allParams['index']))
        else:
            resourcePath = re.sub("[&?]index.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
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

        

        

    def GetOutlineCodeByIndex(self, name, index, **kwargs):
        """Get outline code by index.
        Args:
            name (str): The name of the file. (required)

            index (int): Outline code index (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: OutlineCodeResponse
        """

        allParams = dict.fromkeys(['name', 'index', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetOutlineCodeByIndex" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/outlineCodes/{index}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'index' in allParams and allParams['index'] is not None:
            resourcePath = resourcePath.replace("{" + "index" + "}" , str(allParams['index']))
        else:
            resourcePath = re.sub("[&?]index.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'OutlineCodeResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetOutlineCodes(self, name, **kwargs):
        """Read outline codes.
        Args:
            name (str): The name of the file. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: OutlineCodeItemsResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetOutlineCodes" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/outlineCodes/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'OutlineCodeItemsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetReportPdf(self, name, type, **kwargs):
        """Returns created report in PDF format.
        Args:
            name (str): The name of the file. (required)

            type (ReportType): A type of the project's graphical report. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ResponseMessage
        """

        allParams = dict.fromkeys(['name', 'type', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetReportPdf" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/report/?appSid={appSid}&amp;type={type}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'type' in allParams and allParams['type'] is not None:
            resourcePath = resourcePath.replace("{" + "type" + "}" , str(allParams['type']))
        else:
            resourcePath = re.sub("[&?]type.*?(?=&|\\?|$)", "", resourcePath)
        

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

        

        

    def DeleteProjectResource(self, name, resourceUid, **kwargs):
        """Deletes a project resource with all references to it
        Args:
            name (str): The name of the file. (required)

            resourceUid (int): Resource Uid (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'resourceUid', 'storage', 'folder', 'fileName'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteProjectResource" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/resources/{resourceUid}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}&amp;fileName={fileName}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'resourceUid' in allParams and allParams['resourceUid'] is not None:
            resourcePath = resourcePath.replace("{" + "resourceUid" + "}" , str(allParams['resourceUid']))
        else:
            resourcePath = re.sub("[&?]resourceUid.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
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

        

        

    def GetProjectResource(self, name, resourceUid, **kwargs):
        """Get project resource.
        Args:
            name (str): The name of the file. (required)

            resourceUid (int): Resource Uid (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ResourceResponse
        """

        allParams = dict.fromkeys(['name', 'resourceUid', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetProjectResource" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/resources/{resourceUid}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'resourceUid' in allParams and allParams['resourceUid'] is not None:
            resourcePath = resourcePath.replace("{" + "resourceUid" + "}" , str(allParams['resourceUid']))
        else:
            resourcePath = re.sub("[&?]resourceUid.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResourceResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetProjectResources(self, name, **kwargs):
        """Read project resources.
        Args:
            name (str): The name of the file. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ResourceItemsResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetProjectResources" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/resources/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResourceItemsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetResourceAssignments(self, name, resourceUid, **kwargs):
        """Get resource assignments.
        Args:
            name (str): The name of the file. (required)

            resourceUid (int): Resource Uid (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: AssignmentsResponse
        """

        allParams = dict.fromkeys(['name', 'resourceUid', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetResourceAssignments" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/resources/{resourceUid}/assignments/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'resourceUid' in allParams and allParams['resourceUid'] is not None:
            resourcePath = resourcePath.replace("{" + "resourceUid" + "}" , str(allParams['resourceUid']))
        else:
            resourcePath = re.sub("[&?]resourceUid.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'AssignmentsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostProjectResource(self, name, **kwargs):
        """Add a new resource to a project.
        Args:
            name (str): The name of the file. (required)

            resourceName (str): The name of the new resource. The default value is an empty string (optional)

            beforeResourceId (int): The id of the resource to insert the new resource before. The default value is the id of the last resource in a project file. (optional)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: ResourceItemResponse
        """

        allParams = dict.fromkeys(['name', 'resourceName', 'beforeResourceId', 'fileName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostProjectResource" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/resources/?appSid={appSid}&amp;resourceName={resourceName}&amp;beforeResourceId={beforeResourceId}&amp;fileName={fileName}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'resourceName' in allParams and allParams['resourceName'] is not None:
            resourcePath = resourcePath.replace("{" + "resourceName" + "}" , str(allParams['resourceName']))
        else:
            resourcePath = re.sub("[&?]resourceName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'beforeResourceId' in allParams and allParams['beforeResourceId'] is not None:
            resourcePath = resourcePath.replace("{" + "beforeResourceId" + "}" , str(allParams['beforeResourceId']))
        else:
            resourcePath = re.sub("[&?]beforeResourceId.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'ResourceItemResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteProjectTask(self, name, taskUid, **kwargs):
        """Deletes a project task with all references to it and rebuilds tasks tree.
        Args:
            name (str): The name of the file. (required)

            taskUid (int): Task Uid (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'taskUid', 'storage', 'folder', 'fileName'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteProjectTask" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/tasks/{taskUid}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}&amp;fileName={fileName}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'taskUid' in allParams and allParams['taskUid'] is not None:
            resourcePath = resourcePath.replace("{" + "taskUid" + "}" , str(allParams['taskUid']))
        else:
            resourcePath = re.sub("[&?]taskUid.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
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

        

        

    def GetProjectTask(self, name, taskUid, **kwargs):
        """Read project task.
        Args:
            name (str): The name of the file. (required)

            taskUid (int): Task Uid (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: TaskResponse
        """

        allParams = dict.fromkeys(['name', 'taskUid', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetProjectTask" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/tasks/{taskUid}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'taskUid' in allParams and allParams['taskUid'] is not None:
            resourcePath = resourcePath.replace("{" + "taskUid" + "}" , str(allParams['taskUid']))
        else:
            resourcePath = re.sub("[&?]taskUid.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'TaskResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetProjectTasks(self, name, **kwargs):
        """Read project task items.
        Args:
            name (str): The name of the file. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: TaskItemsResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetProjectTasks" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/tasks/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'TaskItemsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def GetTaskAssignments(self, name, taskUid, **kwargs):
        """Get task assignments.
        Args:
            name (str): The name of the file. (required)

            taskUid (int): Task Uid (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: AssignmentsResponse
        """

        allParams = dict.fromkeys(['name', 'taskUid', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetTaskAssignments" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/tasks/{taskUid}/assignments/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'taskUid' in allParams and allParams['taskUid'] is not None:
            resourcePath = resourcePath.replace("{" + "taskUid" + "}" , str(allParams['taskUid']))
        else:
            resourcePath = re.sub("[&?]taskUid.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'AssignmentsResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostProjectTask(self, name, **kwargs):
        """Add a new task to a project.
        Args:
            name (str): The name of the file. (required)

            taskName (str): The name of the new task. The default value is an empty string (optional)

            beforeTaskId (int): The id of the task to insert the new task before. The default value is the id of the last task in a project file. (optional)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: TaskItemResponse
        """

        allParams = dict.fromkeys(['name', 'taskName', 'beforeTaskId', 'fileName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostProjectTask" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/tasks/?appSid={appSid}&amp;taskName={taskName}&amp;beforeTaskId={beforeTaskId}&amp;fileName={fileName}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'taskName' in allParams and allParams['taskName'] is not None:
            resourcePath = resourcePath.replace("{" + "taskName" + "}" , str(allParams['taskName']))
        else:
            resourcePath = re.sub("[&?]taskName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'beforeTaskId' in allParams and allParams['beforeTaskId'] is not None:
            resourcePath = resourcePath.replace("{" + "beforeTaskId" + "}" , str(allParams['beforeTaskId']))
        else:
            resourcePath = re.sub("[&?]beforeTaskId.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'TaskItemResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def DeleteTaskLink(self, name, index, **kwargs):
        """Updates task link.
        Args:
            name (str): The name of the file. (required)

            index (int): Task link index (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'index', 'storage', 'folder', 'fileName'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteTaskLink" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/taskLinks/{index}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}&amp;fileName={fileName}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'index' in allParams and allParams['index'] is not None:
            resourcePath = resourcePath.replace("{" + "index" + "}" , str(allParams['index']))
        else:
            resourcePath = re.sub("[&?]index.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'DELETE'
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

        

        

    def GetTaskLinks(self, name, **kwargs):
        """Read task links.
        Args:
            name (str): The name of the file. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            

        Returns: TaskLinksResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetTaskLinks" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/taskLinks/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
                responseObject = self.apiClient.pre_deserialize(response.content, 'TaskLinksResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        

        

    def PostTaskLink(self, name, body, **kwargs):
        """Adds a new task link to a project.
        Args:
            name (str): The name of the file. (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            body (TaskLink): TaskLink dto (required)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder', 'fileName', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PostTaskLink" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/taskLinks/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}&amp;fileName={fileName}'
        
    
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
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'POST'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

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

        

        

    def PutTaskLink(self, name, index, body, **kwargs):
        """Updates task link.
        Args:
            name (str): The name of the file. (required)

            index (int): Task link index (required)

            storage (str): The document storage. (optional)

            folder (str): The document folder. (optional)

            fileName (str): The name of the project document to save changes to. If this parameter is omitted then the changes will be saved to the source project document. (optional)

            body (TaskLink): TaskLink dto (required)

            

        Returns: TaskLinkResponse
        """

        allParams = dict.fromkeys(['name', 'index', 'storage', 'folder', 'fileName', 'body'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutTaskLink" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/taskLinks/{index}/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}&amp;fileName={fileName}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'index' in allParams and allParams['index'] is not None:
            resourcePath = resourcePath.replace("{" + "index" + "}" , str(allParams['index']))
        else:
            resourcePath = re.sub("[&?]index.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = body

        headerParams['Accept'] = 'application/xml,application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'TaskLinkResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        
    def PutMoveTask(self, name, taskUid, parentTaskUid, **kwargs):
        """
        Args:
            name (str):  (required)

            taskUid (int):  (required)

            parentTaskUid (int):  (required)

            fileName (str):  (optional)

            storage (str):  (optional)

            folder (str):  (optional)

            

        Returns: SaaSposeResponse
        """

        allParams = dict.fromkeys(['name', 'taskUid', 'parentTaskUid', 'fileName', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method PutMoveTask" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/tasks/{taskUid}/move/?parentTaskUid={parentTaskUid}&amp;appSid={appSid}&amp;fileName={fileName}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'taskUid' in allParams and allParams['taskUid'] is not None:
            resourcePath = resourcePath.replace("{" + "taskUid" + "}" , str(allParams['taskUid']))
        else:
            resourcePath = re.sub("[&?]taskUid.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'parentTaskUid' in allParams and allParams['parentTaskUid'] is not None:
            resourcePath = resourcePath.replace("{" + "parentTaskUid" + "}" , str(allParams['parentTaskUid']))
        else:
            resourcePath = re.sub("[&?]parentTaskUid.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'fileName' in allParams and allParams['fileName'] is not None:
            resourcePath = resourcePath.replace("{" + "fileName" + "}" , str(allParams['fileName']))
        else:
            resourcePath = re.sub("[&?]fileName.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'storage' in allParams and allParams['storage'] is not None:
            resourcePath = resourcePath.replace("{" + "storage" + "}" , str(allParams['storage']))
        else:
            resourcePath = re.sub("[&?]storage.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'folder' in allParams and allParams['folder'] is not None:
            resourcePath = resourcePath.replace("{" + "folder" + "}" , str(allParams['folder']))
        else:
            resourcePath = re.sub("[&?]folder.*?(?=&|\\?|$)", "", resourcePath)
        

        method = 'PUT'
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

        
    def GetTaskRecurringInfo(self, name, taskUid, **kwargs):
        """
        Args:
            name (str):  (required)

            taskUid (int):  (required)

            storage (str):  (optional)

            folder (str):  (optional)

            

        Returns: RecurringInfoResponse
        """

        allParams = dict.fromkeys(['name', 'taskUid', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetTaskRecurringInfo" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/tasks/{taskUid}/recurringInfo/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
        resourcePath = resourcePath.replace('&amp;','&').replace("/?","?").replace("toFormat={toFormat}","format={format}").replace("{path}","{Path}")

        if 'name' in allParams and allParams['name'] is not None:
            resourcePath = resourcePath.replace("{" + "name" + "}" , str(allParams['name']))
        else:
            resourcePath = re.sub("[&?]name.*?(?=&|\\?|$)", "", resourcePath)
        

        if 'taskUid' in allParams and allParams['taskUid'] is not None:
            resourcePath = resourcePath.replace("{" + "taskUid" + "}" , str(allParams['taskUid']))
        else:
            resourcePath = re.sub("[&?]taskUid.*?(?=&|\\?|$)", "", resourcePath)
        

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
                responseObject = self.apiClient.pre_deserialize(response.content, 'RecurringInfoResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)



    def GetProjectWbsDefinition(self, name, **kwargs):
        """
        Args:
            name (str):  (required)

            storage (str):  (optional)

            folder (str):  (optional)

            

        Returns: WBSDefinitionResponse
        """

        allParams = dict.fromkeys(['name', 'storage', 'folder'])

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetProjectWbsDefinition" % key)
            params[key] = val
        
        for (key, val) in params.iteritems():
            if key in allParams:
                allParams[key] = val
        
        resourcePath = '/tasks/{name}/wbsDefinition/?appSid={appSid}&amp;storage={storage}&amp;folder={folder}'
        
    
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
        

        method = 'GET'
        queryParams = {}
        headerParams = {}
        formParams = {}
        files = { }
        bodyParam = None

        headerParams['Accept'] = 'application/json'
        headerParams['Content-Type'] = 'application/json'

        postData = (formParams if formParams else bodyParam)

        response =  self.apiClient.callAPI(resourcePath, method, queryParams, postData, headerParams, files=files)

        try:
            if response.status_code in [200,201,202]:
                responseObject = self.apiClient.pre_deserialize(response.content, 'WBSDefinitionResponse', response.headers['content-type'])
                return responseObject
            else:
                raise ApiException(response.status_code,response.content)
        except Exception:
            raise ApiException(response.status_code,response.content)

        
        


        

    




