#!/usr/bin/env python
# coding: utf-8

"""
CustomersApi.py
Copyright 2015 SmartBear Software

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
from __future__ import absolute_import

import sys
import os
import urllib

# python 2 and python 3 compatibility library
from six import iteritems

from .. import configuration
from ..api_client import ApiClient

class CustomersApi(object):

    def __init__(self, api_client=None):
        if api_client:
            self.api_client = api_client
        else:
            if not configuration.api_client:
                configuration.api_client = ApiClient('https://localhost/')
            self.api_client = configuration.api_client
        # Authentication methods
        self.auth_settings = ['oauth2']
    
    
    def list(self, **kwargs):
        """
        Get a list of customers.
        

        :param int limit: How many results to return. 
        :param int offset: How many results to skip. 
        
        :return: CustomerListResponse
        """
        
        all_params = ['limit', 'offset']

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method list" % key)
            params[key] = val
        del params['kwargs']

        resource_path = '/customers'.replace('{format}', 'json')
        method = 'GET'

        path_params = {}
        
        query_params = {}
        
        if 'limit' in params:
            query_params['limit'] = params['limit']
        
        if 'offset' in params:
            query_params['offset'] = params['offset']
        
        header_params = {}
        
        form_params = {}
        files = {}
        
        body_params = None
        
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/vnd.dwolla.v1.hal+json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type([])


        response = self.api_client.call_api(resource_path, method, path_params, query_params, header_params,
                                            body=body_params, post_params=form_params, files=files,
                                            response='CustomerListResponse', auth_settings=self.auth_settings)
        
        return response
        
    def create(self, **kwargs):
        """
        Create a new customer.
        

        :param CreateCustomer body: Customer to create. 
        
        :return: Unit
        """
        
        all_params = ['body']

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method create" % key)
            params[key] = val
        del params['kwargs']

        resource_path = '/customers'.replace('{format}', 'json')
        method = 'POST'

        path_params = {}
        
        query_params = {}
        
        header_params = {}
        
        form_params = {}
        files = {}
        
        body_params = None
        
        if 'body' in params:
            body_params = params['body']
        
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/vnd.dwolla.v1.hal+json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(['application/vnd.dwolla.v1.hal+json'])


        response = self.api_client.call_api(resource_path, method, path_params, query_params, header_params,
                                            body=body_params, post_params=form_params, files=files,
                                            response='Unit', auth_settings=self.auth_settings)
        
        return response
        
    def get_customer(self, id, **kwargs):
        """
        Get a customer by id
        

        :param str id: Id of customer to get. (required)
        
        :return: Customer
        """
        
        # verify the required parameter 'id' is set
        if id is None:
            raise ValueError("Missing the required parameter `id` when calling `get_customer`")
        
        all_params = ['id']

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method get_customer" % key)
            params[key] = val
        del params['kwargs']

        resource_path = '/customers/{id}'.replace('{format}', 'json')
        method = 'GET'

        path_params = {}
        
        if 'id' in params:
            path_params['id'] = params['id']  
        
        query_params = {}
        
        header_params = {}
        
        form_params = {}
        files = {}
        
        body_params = None
        
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/vnd.dwolla.v1.hal+json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(['application/vnd.dwolla.v1.hal+json'])


        response = self.api_client.call_api(resource_path, method, path_params, query_params, header_params,
                                            body=body_params, post_params=form_params, files=files,
                                            response='Customer', auth_settings=self.auth_settings)
        
        return response
        
    def update_customer(self, id, **kwargs):
        """
        Update customer record. Personal customer records are re-verified upon update.
        

        :param UpdateCustomer body: Customer to update. 
        :param str id: Id of customer to update. (required)
        
        :return: Customer
        """
        
        # verify the required parameter 'id' is set
        if id is None:
            raise ValueError("Missing the required parameter `id` when calling `update_customer`")
        
        all_params = ['body', 'id']

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method update_customer" % key)
            params[key] = val
        del params['kwargs']

        resource_path = '/customers/{id}'.replace('{format}', 'json')
        method = 'POST'

        path_params = {}
        
        if 'id' in params:
            path_params['id'] = params['id']  
        
        query_params = {}
        
        header_params = {}
        
        form_params = {}
        files = {}
        
        body_params = None
        
        if 'body' in params:
            body_params = params['body']
        
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/vnd.dwolla.v1.hal+json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(['application/vnd.dwolla.v1.hal+json'])


        response = self.api_client.call_api(resource_path, method, path_params, query_params, header_params,
                                            body=body_params, post_params=form_params, files=files,
                                            response='Customer', auth_settings=self.auth_settings)
        
        return response
        
    def get_customer_documents(self, id, **kwargs):
        """
        Get documents uploaded for customer.
        

        :param str id: ID of customer. (required)
        
        :return: DocumentListResponse
        """
        
        # verify the required parameter 'id' is set
        if id is None:
            raise ValueError("Missing the required parameter `id` when calling `get_customer_documents`")
        
        all_params = ['id']

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method get_customer_documents" % key)
            params[key] = val
        del params['kwargs']

        resource_path = '/customers/{id}/documents'.replace('{format}', 'json')
        method = 'GET'

        path_params = {}
        
        if 'id' in params:
            path_params['id'] = params['id']  
        
        query_params = {}
        
        header_params = {}
        
        form_params = {}
        files = {}
        
        body_params = None
        
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(['application/vnd.dwolla.v1.hal+json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type([])


        response = self.api_client.call_api(resource_path, method, path_params, query_params, header_params,
                                            body=body_params, post_params=form_params, files=files,
                                            response='DocumentListResponse', auth_settings=self.auth_settings)
        
        return response
        
    def upload_document(self, **kwargs):
        """
        Upload a verification document.
        

        
        :return: Unit
        """
        
        all_params = []

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError("Got an unexpected keyword argument '%s' to method upload_document" % key)
            params[key] = val
        del params['kwargs']

        resource_path = '/customers/{id}/documents'.replace('{format}', 'json')
        method = 'POST'

        path_params = {}
        
        query_params = {}
        
        header_params = {}
        
        form_params = {}
        files = {}
        
        body_params = None
        
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept([])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(['multipart/form-data'])


        response = self.api_client.call_api(resource_path, method, path_params, query_params, header_params,
                                            body=body_params, post_params=form_params, files=files,
                                            response='Unit', auth_settings=self.auth_settings)
        
        return response
        









