#!/usr/bin/env python
"""
Copyright 2012 GroupDocs.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

NOTE: This class is auto generated by the swagger code generator program. Do not edit the class manually.
"""
import sys
import os

from models import *
from groupdocs.FileStream import FileStream
from groupdocs.ApiClient import ApiException

class AsyncApi(object):

    def __init__(self, apiClient):
        self.apiClient = apiClient
        self.__basePath = "https://api.groupdocs.com/v2.0"

    @property
    def basePath(self):
        return self.__basePath
    
    @basePath.setter
    def basePath(self, value):
        self.__basePath = value

    
    def GetJobJson(self, userId, jobId, **kwargs):
        """Get job json

        Args:
            userId, str: User GUID (required)
            jobId, str: Job id (required)
            
        Returns: GetJobResponse
        """
        if( userId == None or jobId == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'jobId']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetJobJson" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/jobs/{jobId}'.replace('*', '')
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'GET'

        queryParams = {}
        headerParams = {}

        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        if ('jobId' in params):
            replacement = str(self.apiClient.toPathValue(params['jobId']))
            resourcePath = resourcePath.replace('{' + 'jobId' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'GetJobResponse')
        return responseObject
        
        
    def GetJobResources(self, userId, statusIds, **kwargs):
        """Get job resources

        Args:
            userId, str: User GUID (required)
            statusIds, str: Comma separated job status identifiers (required)
            actions, str: Actions (optional)
            excludedActions, str: Excluded actions (optional)
            
        Returns: GetJobResourcesResponse
        """
        if( userId == None or statusIds == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'statusIds', 'actions', 'excludedActions']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetJobResources" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/jobs/resources?statusIds={statusIds}&actions={actions}&excluded_actions={excludedActions}'.replace('*', '')
        pos = resourcePath.find("?")
        if pos != -1:
            resourcePath = resourcePath[0:pos]
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'GET'

        queryParams = {}
        headerParams = {}

        if ('statusIds' in params):
            queryParams['statusIds'] = self.apiClient.toPathValue(params['statusIds'])
        if ('actions' in params):
            queryParams['actions'] = self.apiClient.toPathValue(params['actions'])
        if ('excludedActions' in params):
            queryParams['excluded_actions'] = self.apiClient.toPathValue(params['excludedActions'])
        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'GetJobResourcesResponse')
        return responseObject
        
        
    def GetJobDocuments(self, userId, jobId, **kwargs):
        """Get job documents

        Args:
            userId, str: User GUID (required)
            jobId, str: Job id or guid (required)
            format, str: Format (optional)
            
        Returns: GetJobDocumentsResponse
        """
        if( userId == None or jobId == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'jobId', 'format']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetJobDocuments" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/jobs/{jobId}/documents?format={format}'.replace('*', '')
        pos = resourcePath.find("?")
        if pos != -1:
            resourcePath = resourcePath[0:pos]
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'GET'

        queryParams = {}
        headerParams = {}

        if ('format' in params):
            queryParams['format'] = self.apiClient.toPathValue(params['format'])
        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        if ('jobId' in params):
            replacement = str(self.apiClient.toPathValue(params['jobId']))
            resourcePath = resourcePath.replace('{' + 'jobId' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'GetJobDocumentsResponse')
        return responseObject
        
        
    def CreateJob(self, userId, body, **kwargs):
        """Create job

        Args:
            userId, str: User GUID (required)
            body, JobInfo: Job (required)
            
        Returns: CreateJobResponse
        """
        if( userId == None or body == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'body']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method CreateJob" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/jobs'.replace('*', '')
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'POST'

        queryParams = {}
        headerParams = {}

        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'CreateJobResponse')
        return responseObject
        
        
    def DeleteJob(self, userId, jobGuid, **kwargs):
        """Delete draft job

        Args:
            userId, str: User GUID (required)
            jobGuid, str: Job Guid (required)
            
        Returns: DeleteResult
        """
        if( userId == None or jobGuid == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'jobGuid']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteJob" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/jobs/{jobGuid}'.replace('*', '')
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'DELETE'

        queryParams = {}
        headerParams = {}

        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        if ('jobGuid' in params):
            replacement = str(self.apiClient.toPathValue(params['jobGuid']))
            resourcePath = resourcePath.replace('{' + 'jobGuid' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'DeleteResult')
        return responseObject
        
        
    def AddJobDocument(self, userId, jobId, fileId, checkOwnership, **kwargs):
        """Add job document

        Args:
            userId, str: User GUID (required)
            jobId, str: Job id or guid (required)
            fileId, str: File GUID (required)
            checkOwnership, bool: Check Document Ownership (required)
            formats, str: Formats (optional)
            
        Returns: AddJobDocumentResponse
        """
        if( userId == None or jobId == None or fileId == None or checkOwnership == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'jobId', 'fileId', 'checkOwnership', 'formats']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method AddJobDocument" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/jobs/{jobId}/files/{fileId}?check_ownership={checkOwnership}&out_formats={formats}'.replace('*', '')
        pos = resourcePath.find("?")
        if pos != -1:
            resourcePath = resourcePath[0:pos]
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'PUT'

        queryParams = {}
        headerParams = {}

        if ('checkOwnership' in params):
            queryParams['check_ownership'] = self.apiClient.toPathValue(params['checkOwnership'])
        if ('formats' in params):
            queryParams['out_formats'] = self.apiClient.toPathValue(params['formats'])
        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        if ('jobId' in params):
            replacement = str(self.apiClient.toPathValue(params['jobId']))
            resourcePath = resourcePath.replace('{' + 'jobId' + '}',
                                                replacement)
        if ('fileId' in params):
            replacement = str(self.apiClient.toPathValue(params['fileId']))
            resourcePath = resourcePath.replace('{' + 'fileId' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'AddJobDocumentResponse')
        return responseObject
        
        
    def DeleteJobDocument(self, userId, jobGuid, documentId, **kwargs):
        """Delete document from job

        Args:
            userId, str: User GUID (required)
            jobGuid, str: Job Guid (required)
            documentId, str: Document GUID (required)
            
        Returns: DeleteResponse
        """
        if( userId == None or jobGuid == None or documentId == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'jobGuid', 'documentId']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method DeleteJobDocument" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/jobs/{jobGuid}/documents/{documentId}'.replace('*', '')
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'DELETE'

        queryParams = {}
        headerParams = {}

        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        if ('jobGuid' in params):
            replacement = str(self.apiClient.toPathValue(params['jobGuid']))
            resourcePath = resourcePath.replace('{' + 'jobGuid' + '}',
                                                replacement)
        if ('documentId' in params):
            replacement = str(self.apiClient.toPathValue(params['documentId']))
            resourcePath = resourcePath.replace('{' + 'documentId' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'DeleteResponse')
        return responseObject
        
        
    def AddJobDocumentUrl(self, userId, jobId, absoluteUrl, **kwargs):
        """Add job document url

        Args:
            userId, str: User GUID (required)
            jobId, str: Job id (required)
            absoluteUrl, str: Absolute Url (required)
            formats, str: Formats (optional)
            
        Returns: AddJobDocumentResponse
        """
        if( userId == None or jobId == None or absoluteUrl == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'jobId', 'absoluteUrl', 'formats']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method AddJobDocumentUrl" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/jobs/{jobId}/urls?absolute_url={absoluteUrl}&out_formats={formats}'.replace('*', '')
        pos = resourcePath.find("?")
        if pos != -1:
            resourcePath = resourcePath[0:pos]
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'PUT'

        queryParams = {}
        headerParams = {}

        if ('absoluteUrl' in params):
            queryParams['absolute_url'] = self.apiClient.toPathValue(params['absoluteUrl'])
        if ('formats' in params):
            queryParams['out_formats'] = self.apiClient.toPathValue(params['formats'])
        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        if ('jobId' in params):
            replacement = str(self.apiClient.toPathValue(params['jobId']))
            resourcePath = resourcePath.replace('{' + 'jobId' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'AddJobDocumentResponse')
        return responseObject
        
        
    def UpdateJob(self, userId, jobId, body, **kwargs):
        """Update job

        Args:
            userId, str: User GUID (required)
            jobId, str: Job id or Guid (required)
            body, JobInfo: Job (required)
            
        Returns: UpdateJobResponse
        """
        if( userId == None or jobId == None or body == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'jobId', 'body']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method UpdateJob" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/jobs/{jobId}'.replace('*', '')
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'PUT'

        queryParams = {}
        headerParams = {}

        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        if ('jobId' in params):
            replacement = str(self.apiClient.toPathValue(params['jobId']))
            resourcePath = resourcePath.replace('{' + 'jobId' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'UpdateJobResponse')
        return responseObject
        
        
    def GetJobs(self, userId, **kwargs):
        """Get jobs

        Args:
            userId, str: User GUID (required)
            pageIndex, str: Page Index (optional)
            pageSize, str: Page Size (optional)
            datetime, str: Date (optional)
            statusIds, str: Comma separated status identifiers (optional)
            actions, str: Actions (optional)
            excludedActions, str: Excluded actions (optional)
            jobName, str: Filtred job name (optional)
            orderBy, str: Sorded column name (optional)
            orderAsc, bool: Order ASC (optional)
            
        Returns: GetJobsResponse
        """
        if( userId == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'pageIndex', 'pageSize', 'datetime', 'statusIds', 'actions', 'excludedActions', 'jobName', 'orderBy', 'orderAsc']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetJobs" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/jobs?page={pageIndex}&count={pageSize}&date={date}&statusIds={statusIds}&actions={actions}&excluded_actions={excludedActions}&jobName={jobName}&order_by={orderBy}&order_asc={orderAsc}'.replace('*', '')
        pos = resourcePath.find("?")
        if pos != -1:
            resourcePath = resourcePath[0:pos]
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'GET'

        queryParams = {}
        headerParams = {}

        if ('pageIndex' in params):
            queryParams['page'] = self.apiClient.toPathValue(params['pageIndex'])
        if ('pageSize' in params):
            queryParams['count'] = self.apiClient.toPathValue(params['pageSize'])
        if ('datetime' in params):
            queryParams['date'] = self.apiClient.toPathValue(params['datetime'])
        if ('statusIds' in params):
            queryParams['statusIds'] = self.apiClient.toPathValue(params['statusIds'])
        if ('actions' in params):
            queryParams['actions'] = self.apiClient.toPathValue(params['actions'])
        if ('excludedActions' in params):
            queryParams['excluded_actions'] = self.apiClient.toPathValue(params['excludedActions'])
        if ('jobName' in params):
            queryParams['jobName'] = self.apiClient.toPathValue(params['jobName'])
        if ('orderBy' in params):
            queryParams['order_by'] = self.apiClient.toPathValue(params['orderBy'])
        if ('orderAsc' in params):
            queryParams['order_asc'] = self.apiClient.toPathValue(params['orderAsc'])
        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'GetJobsResponse')
        return responseObject
        
        
    def GetJobsDocuments(self, userId, **kwargs):
        """Get jobs documents

        Args:
            userId, str: User GUID (required)
            pageIndex, str: Page Index (optional)
            pageSize, str: Page Size (optional)
            actions, str: Actions (optional)
            excludedActions, str: Excluded actions (optional)
            orderBy, str: Order by (optional)
            orderAsc, bool: Order asc (optional)
            
        Returns: GetJobsDocumentsResponse
        """
        if( userId == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'pageIndex', 'pageSize', 'actions', 'excludedActions', 'orderBy', 'orderAsc']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetJobsDocuments" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/jobs/documents?page={pageIndex}&count={pageSize}&actions={actions}&excluded_actions={excludedActions}&order_by={orderBy}&order_asc={orderAsc}'.replace('*', '')
        pos = resourcePath.find("?")
        if pos != -1:
            resourcePath = resourcePath[0:pos]
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'GET'

        queryParams = {}
        headerParams = {}

        if ('pageIndex' in params):
            queryParams['page'] = self.apiClient.toPathValue(params['pageIndex'])
        if ('pageSize' in params):
            queryParams['count'] = self.apiClient.toPathValue(params['pageSize'])
        if ('actions' in params):
            queryParams['actions'] = self.apiClient.toPathValue(params['actions'])
        if ('excludedActions' in params):
            queryParams['excluded_actions'] = self.apiClient.toPathValue(params['excludedActions'])
        if ('orderBy' in params):
            queryParams['order_by'] = self.apiClient.toPathValue(params['orderBy'])
        if ('orderAsc' in params):
            queryParams['order_asc'] = self.apiClient.toPathValue(params['orderAsc'])
        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'GetJobsDocumentsResponse')
        return responseObject
        
        
    def Convert(self, userId, fileId, **kwargs):
        """Convert

        Args:
            userId, str: User GUID (required)
            fileId, str: File GUID (required)
            emailResults, str: Email results (optional)
            description, str: Description (optional)
            printScript, bool: Print (optional)
            callbackUrl, str: Callback url (optional)
            new_type, str: Target type (optional)
            
        Returns: ConvertResponse
        """
        if( userId == None or fileId == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'fileId', 'emailResults', 'description', 'printScript', 'callbackUrl', 'new_type']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method Convert" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/files/{fileId}?new_type={targetType}&email_results={emailResults}&new_description={description}&print_script={printScript}&callback={callbackUrl}'.replace('*', '')
        pos = resourcePath.find("?")
        if pos != -1:
            resourcePath = resourcePath[0:pos]
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'POST'

        queryParams = {}
        headerParams = {}

        if ('emailResults' in params):
            queryParams['email_results'] = self.apiClient.toPathValue(params['emailResults'])
        if ('description' in params):
            queryParams['new_description'] = self.apiClient.toPathValue(params['description'])
        if ('printScript' in params):
            queryParams['print_script'] = self.apiClient.toPathValue(params['printScript'])
        if ('callbackUrl' in params):
            queryParams['callback'] = self.apiClient.toPathValue(params['callbackUrl'])
        if ('new_type' in params):
            queryParams['new_type'] = self.apiClient.toPathValue(params['new_type'])
        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        if ('fileId' in params):
            replacement = str(self.apiClient.toPathValue(params['fileId']))
            resourcePath = resourcePath.replace('{' + 'fileId' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'ConvertResponse')
        return responseObject
        
        
    def GetPossibleConversions(self, userId, fileExt, **kwargs):
        """Get Possible Conversions

        Args:
            userId, str: User GUID (required)
            fileExt, str: File extension to check (required)
            
        Returns: GetPossibleConversions
        """
        if( userId == None or fileExt == None ):
            raise ApiException(400, "missing required parameters")
        allParams = ['userId', 'fileExt']

        params = locals()
        for (key, val) in params['kwargs'].iteritems():
            if key not in allParams:
                raise TypeError("Got an unexpected keyword argument '%s' to method GetPossibleConversions" % key)
            params[key] = val
        del params['kwargs']

        resourcePath = '/async/{userId}/possibleConversions/{fileExt}'.replace('*', '')
        resourcePath = resourcePath.replace('{format}', 'json')
        method = 'GET'

        queryParams = {}
        headerParams = {}

        if ('userId' in params):
            replacement = str(self.apiClient.toPathValue(params['userId']))
            resourcePath = resourcePath.replace('{' + 'userId' + '}',
                                                replacement)
        if ('fileExt' in params):
            replacement = str(self.apiClient.toPathValue(params['fileExt']))
            resourcePath = resourcePath.replace('{' + 'fileExt' + '}',
                                                replacement)
        postData = (params['body'] if 'body' in params else None)
        response = self.apiClient.callAPI(self.basePath, resourcePath, method, queryParams,
                                          postData, headerParams)

        if not response:
            return None

        responseObject = self.apiClient.deserialize(response, 'GetPossibleConversions')
        return responseObject
        
        
    


