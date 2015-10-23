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
"""
class SignatureEnvelopeInfo:
    """
    
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually."""


    def __init__(self):
        self.swaggerTypes = {
            'id': 'str',
            'name': 'str',
            'creationDateTime': 'str',
            'updatedDateTime': 'str',
            'ownerGuid': 'str',
            'status': 'int',
            'statusDateTime': 'str',
            'reminderTime': 'float',
            'stepExpireTime': 'float',
            'envelopeExpireTime': 'float',
            'ownerShouldSign': 'bool',
            'orderedSignature': 'bool',
            'emailSubject': 'str',
            'emailBody': 'str',
            'documentsCount': 'float',
            'documentsPages': 'float',
            'recipients': 'list[SignatureEnvelopeRecipientInfo]',
            'waterMarkText': 'str',
            'waterMarkImage': 'str',
            'attachSignedDocument': 'bool',
            'includeViewLink': 'bool',
            'canBeCommented': 'bool',
            'inPersonSign': 'bool',
            'ownerName': 'str',
            'enableTypedSignature': 'bool',
            'enableUploadedSignature': 'bool',
            'requireUserAuthForSign': 'bool',
            'requestUserAuthByPhoto': 'bool',
            'showRecipientCommentInSignedDocument': 'bool',
            'tags': 'str'

        }


        self.id = None # str
        self.name = None # str
        self.creationDateTime = None # str
        self.updatedDateTime = None # str
        self.ownerGuid = None # str
        self.status = None # int
        self.statusDateTime = None # str
        self.reminderTime = None # float
        self.stepExpireTime = None # float
        self.envelopeExpireTime = None # float
        self.ownerShouldSign = None # bool
        self.orderedSignature = None # bool
        self.emailSubject = None # str
        self.emailBody = None # str
        self.documentsCount = None # float
        self.documentsPages = None # float
        self.recipients = None # list[SignatureEnvelopeRecipientInfo]
        self.waterMarkText = None # str
        self.waterMarkImage = None # str
        self.attachSignedDocument = None # bool
        self.includeViewLink = None # bool
        self.canBeCommented = None # bool
        self.inPersonSign = None # bool
        self.ownerName = None # str
        self.enableTypedSignature = None # bool
        self.enableUploadedSignature = None # bool
        self.requireUserAuthForSign = None # bool
        self.requestUserAuthByPhoto = None # bool
        self.showRecipientCommentInSignedDocument = None # bool
        self.tags = None # str
        
