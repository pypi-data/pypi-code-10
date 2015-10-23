#!/usr/bin/env python
# coding: utf-8

"""
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
"""

class WebhookSubscription(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """

    def __init__(self):
        """
        Swagger model

        :param dict swaggerTypes: The key is attribute name and the value is attribute type.
        :param dict attributeMap: The key is attribute name and the value is json key in definition.
        """
        self.swagger_types = {
            '_links': 'dict(String, HalLink)',
            '_embedded': 'dict',
            'id': 'str',
            'url': 'str',
            'created': 'DateTime'
        }

        self.attribute_map = {
            '_links': '_links',
            '_embedded': '_embedded',
            'id': 'id',
            'url': 'url',
            'created': 'created'
        }
        
        
        self._links = None  # dict(String, HalLink)
        
        
        self._embedded = None  # dict
        
        
        self.id = None  # str
        
        
        self.url = None  # str
        
        
        self.created = None  # DateTime
        

    def __repr__(self):
        properties = []
        for p in self.__dict__:
            if p != 'swaggerTypes' and p != 'attributeMap':
                properties.append('{prop}={val!r}'.format(prop=p, val=self.__dict__[p]))

        return '<{name} {props}>'.format(name=__name__, props=' '.join(properties))


