#!/usr/bin/env python

class ExtendedAttributeItemsResponse(object):
    """NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually."""


    def __init__(self):
        """
        Attributes:
          swaggerTypes (dict): The key is attribute name and the value is attribute type.
          attributeMap (dict): The key is attribute name and the value is json key in definition.
        """
        self.swaggerTypes = {
            'ExtendedAttributes': 'ExtendedAttributeItems',
            'Code': 'str',
            'Status': 'str'

        }

        self.attributeMap = {
            'ExtendedAttributes': 'ExtendedAttributes','Code': 'Code','Status': 'Status'}       

        self.ExtendedAttributes = None # ExtendedAttributeItems
        self.Code = None # str
        self.Status = None # str
        
