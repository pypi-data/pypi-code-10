#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2015 HQM <qiminis0801@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import re


class SinicValidate(object):
    def __init__(self):
        # Refer: http://www.oschina.net/code/snippet_238351_48624
        self.ChinaMobile = r'^134[0-8]\d{7}$|^(?:13[5-9]|147|15[0-27-9]|178|18[2-478])\d{8}$'  # 移动方面最新答复
        self.ChinaUnion = r'^(?:13[0-2]|145|15[56]|176|18[56])\d{8}$'  # 向联通微博确认并未回复
        self.ChinaTelcom = r'^(?:133|153|177|18[019])\d{8}$'  # 1349号段 电信方面没给出答复，视作不存在
        self.OtherTelphone = r'^170([059])\d{7}$'  # 其他运营商

        self.email_regex = r'^.+@([^.@][^@]+)$'

    def phone(self, message, china_mobile=None, china_union=None, china_telcom=None, other_telphone=None):
        """
        Validates a phone number.
        :param message:
        :param china_mobile:
        :param china_union:
        :param china_telcom:
        :param other_telphone:
        :return:
        """
        isChinaMobile = isChinaUnion = isChinaTelcom = isOtherTelphone = False
        if re.match(china_mobile or self.ChinaMobile, message):
            isChinaMobile = True
        elif re.match(china_union or self.ChinaUnion, message):
            isChinaUnion = True
        elif re.match(china_telcom or self.ChinaTelcom, message):
            isChinaTelcom = True
        elif re.match(other_telphone or self.OtherTelphone, message):
            isOtherTelphone = True
        return {
            'isPhone': isChinaMobile or isChinaUnion or isChinaTelcom or isOtherTelphone,
            'isChinaMobile': isChinaMobile,
            'isChinaUnion': isChinaUnion,
            'isChinaTelcom': isChinaTelcom,
            'isOtherTelphone': isOtherTelphone,
        }

    def email(self, message, regex=None):
        """
        Validates an email address.
        :param message:
        :param regex:
        :return:
        """
        return re.match(regex or self.email_regex, message)


# For backwards compatibility
_global_instance = SinicValidate()
phone = _global_instance.phone
email = _global_instance.email
