#!/usr/bin/env python
'''
 Licensed to the Apache Software Foundation (ASF) under one
 or more contributor license agreements.  See the NOTICE file
 distributed with this work for additional information
 regarding copyright ownership.  The ASF licenses this file
 to you under the Apache License, Version 2.0 (the
 "License"); you may not use this file except in compliance
 with the License.  You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
'''
__author__ = 'xixi.xxx'

import os
if os.environ.get('LC_CTYPE', '') == 'UTF-8':
    os.environ['LC_CTYPE'] = 'en_US.UTF-8'
import aliyunCompleter

def aliyun_complete():
    cline = os.environ.get('COMP_LINE') or os.environ.get('COMMAND_LINE') or ''
    cpoint = int(os.environ.get('COMP_POINT') or len(cline))
    try:
        aliyunCompleter.complete(cline, cpoint)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    aliyun_complete()
