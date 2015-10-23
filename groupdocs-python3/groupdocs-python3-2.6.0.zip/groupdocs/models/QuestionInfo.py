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
class QuestionInfo:
    """
    
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually."""


    def __init__(self):
        self.swaggerTypes = {
            'field': 'str',
            'text': 'str',
            'def_answer': 'str',
            'required': 'bool',
            'disabled': 'bool',
            'type': 'str',
            'answers': 'list[AnswerInfo]',
            'conditions': 'list[ConditionInfo]',
            'acceptableValues': 'list[str]',
            'max_length': 'int',
            'rect': 'Rectangle',
            'regionName': 'str',
            'hint': 'str',
            'dimension': 'FieldDimension'

        }


        self.field = None # str
        self.text = None # str
        self.def_answer = None # str
        self.required = None # bool
        self.disabled = None # bool
        self.type = None # str
        self.answers = None # list[AnswerInfo]
        self.conditions = None # list[ConditionInfo]
        self.acceptableValues = None # list[str]
        self.max_length = None # int
        self.rect = None # Rectangle
        self.regionName = None # str
        self.hint = None # str
        self.dimension = None # FieldDimension
        
