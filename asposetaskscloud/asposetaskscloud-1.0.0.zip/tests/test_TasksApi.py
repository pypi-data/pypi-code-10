import unittest
import os.path
import json
import inspect
import requests

import asposetaskscloud
from asposetaskscloud.TasksApi import TasksApi
from asposetaskscloud.TasksApi import ApiException
from asposetaskscloud.models import SaaSposeResponse
from asposetaskscloud.models import AssignmentResponse
from asposetaskscloud.models import AssignmentItemsResponse
from asposetaskscloud.models import AssignmentItemResponse
from asposetaskscloud.models import CalendarExceptionsResponse
from asposetaskscloud.models import CalendarResponse
from asposetaskscloud.models import CalendarItemsResponse
from asposetaskscloud.models import CalendarException
from asposetaskscloud.models import Calendar
from asposetaskscloud.models import CalendarItemResponse
from asposetaskscloud.models import TaskItemsResponse
from asposetaskscloud.models import DocumentResponse
from asposetaskscloud.models import DocumentPropertiesResponse
from asposetaskscloud.models import DocumentPropertyResponse
from asposetaskscloud.models import DocumentProperty
from asposetaskscloud.models import ExtendedAttributeResponse
from asposetaskscloud.models import ExtendedAttributeItemsResponse
from asposetaskscloud.models import OutlineCodeResponse
from asposetaskscloud.models import OutlineCodeItemsResponse
from asposetaskscloud.models import ResourceResponse
from asposetaskscloud.models import ResourceItemsResponse
from asposetaskscloud.models import AssignmentsResponse
from asposetaskscloud.models import ResourceItemResponse
from asposetaskscloud.models import TaskResponse
from asposetaskscloud.models import TaskItemResponse
from asposetaskscloud.models import TaskLinksResponse
from asposetaskscloud.models import TaskLink
from asposetaskscloud.models import TaskLinkResponse
from asposetaskscloud.models import RecurringInfoResponse
from asposetaskscloud.models import WBSDefinitionResponse

import asposestoragecloud 
from asposestoragecloud.StorageApi import StorageApi


import random
import string

class TestAsposeSlidesCloud(unittest.TestCase):

    def setUp(self):

        with open('setup.json') as json_file:
            data = json.load(json_file)

        self.storageApiClient = asposestoragecloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.storageApi = StorageApi(self.storageApiClient)

        self.apiClient = asposetaskscloud.ApiClient.ApiClient(apiKey=str(data['app_key']),appSid=str(data['app_sid']),debug=True,apiServer=str(data['product_uri']))
        self.tasksApi = TasksApi(self.apiClient)

        self.output_path = str(data['output_location'])

    def testDeleteProjectAssignment(self):

        try:
            name =  "sample-project-2.mpp"
            assignmentUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.DeleteProjectAssignment(name, assignmentUid)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetProjectAssignment(self):
        
        try:
            name = "sample-project-2.mpp"
            assignmentUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetProjectAssignment(name, assignmentUid)            

            self.assertIsInstance(response,AssignmentResponse.AssignmentResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetProjectAssignments(self):

        try:
            name = "sample-project-2.mpp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetProjectAssignments(name)            

            self.assertIsInstance(response,AssignmentItemsResponse.AssignmentItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPostProjectAssignment(self):

        try:
            name = "sample-project.mpp"
            taskUid = 1
            resourceUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.PostProjectAssignment(name, taskUid, resourceUid)            

            self.assertIsInstance(response,AssignmentItemResponse.AssignmentItemResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testDeleteCalendarException(self):

        try:
            name = "sample-project.mpp"
            calendarUid = 1
            index = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.DeleteCalendarException(name, calendarUid, index)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testDeleteProjectCalendar(self):

        try:
            name =  "sample-project.mpp"
            calendarUid = 2
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.DeleteProjectCalendar(name, calendarUid)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetCalendarExceptions(self):

        try:
            name =  "sample-project.mpp"
            calendarUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetCalendarExceptions(name, calendarUid)            

            self.assertIsInstance(response,CalendarExceptionsResponse.CalendarExceptionsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetProjectCalendar(self):

        try:
            name =  "sample-project.mpp"
            calendarUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetProjectCalendar(name, calendarUid)            

            self.assertIsInstance(response,CalendarResponse.CalendarResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetProjectCalendars(self):

        try:
            name =  "sample-project.mpp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetProjectCalendars(name)            

            self.assertIsInstance(response,CalendarItemsResponse.CalendarItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPostCalendarExceptions(self):

        try:
            name =  "sample-project-2.mpp"
            calendarUid = 1
            
            body = CalendarException.CalendarException()
            body.Name = "Test"
            body.FromDate = "2015-10-20"
            body.ToDate = "2015-10-22"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.PostCalendarExceptions(name, calendarUid, body)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'Created')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPostProjectCalendar(self):

        try:
            name =  "sample-project.mpp"
            
            body = Calendar.Calendar()
            body.Name = "TestCalender"
            body.Uid = 0
            
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.PostProjectCalendar(name, body)            

            self.assertIsInstance(response,CalendarItemResponse.CalendarItemResponse)
            self.assertEqual(response.Status,'Created')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPutCalendarException(self):

        try:
            name =  "sample-project.mpp"
            calendarUid = 1
            index = 1
            
            body = CalendarException.CalendarException()
            body.Name = "Test"
            body.FromDate = "2015-10-20"
            body.ToDate = "2015-10-22"

            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.PutCalendarException(name, calendarUid, index, body)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetCriticalPath(self):

        try:
            name =  "sample-project.mpp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetCriticalPath(name)            

            self.assertIsInstance(response,TaskItemsResponse.TaskItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetTaskDocument(self):

        try:
            name =  "sample-project-2.mpp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetTaskDocument(name)            

            self.assertIsInstance(response,DocumentResponse.DocumentResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetTaskDocumentWithFormat(self):

        try:
            name =  "sample-project.mpp"
            format = "pdf"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetTaskDocumentWithFormat(name, format)            
            
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetDocumentProperties(self):

        try:
            name =  "sample-project.mpp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetDocumentProperties(name)            

            self.assertIsInstance(response,DocumentPropertiesResponse.DocumentPropertiesResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetDocumentProperty(self):

        try:
            name =  "sample-project.mpp"
            propertyName = "Title"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetDocumentProperty(name, propertyName)            

            self.assertIsInstance(response,DocumentPropertyResponse.DocumentPropertyResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPostDocumentProperty(self):

        try:
            name =  "sample-project-2.mpp"
            propertyName = "Title"
            
            body = DocumentProperty.DocumentProperty()
            body.Name = "Title"
            body.Value = "New Title"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.PostDocumentProperty(name, propertyName, body)            

            self.assertIsInstance(response,DocumentPropertyResponse.DocumentPropertyResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPutDocumentProperty(self):

        try:
            name =  "sample-project-2.mpp"
            propertyName = "Title"
            
            body = DocumentProperty.DocumentProperty()
            body.Name = "Title"
            body.Value = "New Title"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.PutDocumentProperty(name, propertyName, body)            

            self.assertIsInstance(response,DocumentPropertyResponse.DocumentPropertyResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testDeleteExtendedAttributeByIndex(self):

        try:
            name =  "ExtendedAttribute.mpp"
            index = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.DeleteExtendedAttributeByIndex(name, index)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
            print ""
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetExtendedAttributeByIndex(self):

        try:
            name =  "ExtendedAttribute.mpp"
            index = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetExtendedAttributeByIndex(name, index)            

            self.assertIsInstance(response,ExtendedAttributeResponse.ExtendedAttributeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetExtendedAttributes(self):

        try:
            name =  "ExtendedAttribute.mpp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetExtendedAttributes(name)            

            self.assertIsInstance(response,ExtendedAttributeItemsResponse.ExtendedAttributeItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testDeleteOutlineCodeByIndex(self):

        try:
            name =  "Outlinecode.mpp"
            index = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.DeleteOutlineCodeByIndex(name, index)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetOutlineCodeByIndex(self):

        try:
            name =  "Outlinecode.mpp"
            index = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetOutlineCodeByIndex(name, index)            

            self.assertIsInstance(response,OutlineCodeResponse.OutlineCodeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetOutlineCodes(self):

        try:
            name =  "Outlinecode.mpp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetOutlineCodes(name)            

            self.assertIsInstance(response,OutlineCodeItemsResponse.OutlineCodeItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetReportPdf(self):        

        try:
            name =  "sample-project.mpp"
            type = "WorkOverview"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetReportPdf(name, type)            

            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testDeleteProjectResource(self):

        try:
            name =  "sample-project.mpp"
            resourceUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.DeleteProjectResource(name, resourceUid)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetProjectResource(self):

        try:
            name =  "sample-project.mpp"
            resourceUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetProjectResource(name, resourceUid)            

            self.assertIsInstance(response,ResourceResponse.ResourceResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetProjectResources(self):

        try:
            name =  "sample-project.mpp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetProjectResources(name)            

            self.assertIsInstance(response,ResourceItemsResponse.ResourceItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetResourceAssignments(self):

        try:
            name =  "sample-project.mpp"
            resourceUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetResourceAssignments(name, resourceUid)            

            self.assertIsInstance(response,AssignmentsResponse.AssignmentsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPostProjectResource(self):        

        try:
            name =  "sample-project.mpp"
            resourceName = "Resource6"
            beforeResourceId = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.PostProjectResource(name)            

            self.assertIsInstance(response,ResourceItemResponse.ResourceItemResponse)
            self.assertEqual(response.Status,'Created')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testDeleteProjectTask(self):

        try:
            name =  "sample-project.mpp"
            taskUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.DeleteProjectTask(name, taskUid)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetProjectTask(self):

        try:
            name =  "sample-project-2.mpp"
            taskUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetProjectTask(name, taskUid)            

            self.assertIsInstance(response,TaskResponse.TaskResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex



    def testGetProjectTasks(self):

        try:
            name =  "sample-project.mpp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetProjectTasks(name)            

            self.assertIsInstance(response,TaskItemsResponse.TaskItemsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetTaskAssignments(self):        

        try:
            name =  "sample-project-2.mpp"
            taskUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetTaskAssignments(name, taskUid)            

            self.assertIsInstance(response,AssignmentsResponse.AssignmentsResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPostProjectTask(self):

        try:
            name =  "sample-project.mpp"
            taskName = "NewTask"
            beforeTaskId = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.PostProjectTask(name, taskName=taskName, beforeTaskId=beforeTaskId)            

            self.assertIsInstance(response,TaskItemResponse.TaskItemResponse)
            self.assertEqual(response.Status,'Created')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testDeleteTaskLink(self):

        try:
            name =  "sample-project.mpp"
            index = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.DeleteTaskLink(name, index)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetTaskLinks(self):

        try:
            name =  "sample-project-2.mpp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetTaskLinks(name)            

            self.assertIsInstance(response,TaskLinksResponse.TaskLinksResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPostTaskLink(self):

        try:
            name =  "sample-project-2.mpp"
            
            body = TaskLink.TaskLink()
            body.Index = 2
            body.PredecessorUid = 1
            body.SuccessorUid = 2
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.PostTaskLink(name, body)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testPutTaskLink(self):

        try:
            name =  "sample-project.mpp"
            index = 1
            
            body = TaskLink.TaskLink()
            body.Index = 1
            body.PredecessorUid = 0
            body.SuccessorUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.PutTaskLink(name, index, body)            

            self.assertIsInstance(response,TaskLinkResponse.TaskLinkResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

    def testPutMoveTask(self):

        try:
            name =  "sample-project.mpp"
            taskUid = 1
            parentTaskUid = 2
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.PutMoveTask(name, taskUid, parentTaskUid)            

            self.assertIsInstance(response,SaaSposeResponse.SaaSposeResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetTaskRecurringInfo(self):

        try:
            name =  "sample-project.mpp"
            taskUid = 1
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetTaskRecurringInfo(name, taskUid)            

            self.assertIsInstance(response,RecurringInfoResponse.RecurringInfoResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex


    def testGetProjectWbsDefinition(self):

        try:
            name =  "sample-project.mpp"
            
            response = self.storageApi.PutCreate(name,'./data/' + name)
            response = self.tasksApi.GetProjectWbsDefinition(name)            

            self.assertIsInstance(response,WBSDefinitionResponse.WBSDefinitionResponse)
            self.assertEqual(response.Status,'OK')
        
        except ApiException as ex:
            print "Exception"
            print "Code: " + str(ex.code)
            print "Mesage: " + ex.message
            raise ex

if __name__ == '__main__':
    unittest.main()