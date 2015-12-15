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

from __future__ import division

from decimal import Decimal

import random

from .compat import range


ZERO_VALUE = 'Zero Value of Param {0}'
INVALID_VALUE = 'Invalid Value for Num: \'{0}\''
TRIPLE_INVALID_VALUE = 'Invalid Value for Total-{0}, Num-{1}, Min-{2}'


class RedPackets(object):
    def split_dollor_val(self, min, max):
        return min if min > max else Decimal(str(random.randint(min, max)))

    def split_dollor(self, total, num, min=0.01):
        """
        RedPackets Split for Dollor

        :param total: Total Value of RedPackets
        :param num: Split Num of RedPackets
        :param min: Limit Value of Each Split
        """
        if not (total and num):
            raise ValueError(ZERO_VALUE.format('Num' if total else 'Total'))

        # Convert and Check of Total
        total = Decimal(str(total))

        # Convert and Check of Num
        if isinstance(num, float) and int(num) != num:
            raise ValueError(INVALID_VALUE.format(num))
        num = Decimal(str(int(num)))

        # Convert and Check of Min
        min = Decimal(str(min))

        # Compare Total and Num * Min
        if total < num * min:
            raise ValueError(TRIPLE_INVALID_VALUE.format(total, num, min))

        split_list = []
        for i in range(1, int(num)):
            # Random Safety High Limit Total
            safe_total = (total - (num - i) * min) / (num - i)
            split_val = self.split_dollor_val(min * 100, int(safe_total * 100)) / 100
            total -= split_val
            split_list.append(split_val)
        split_list.append(total)

        # Random Disarrange
        random.shuffle(split_list)

        return split_list

    def split_cent_val(self, min, max):
        return min if min > max else random.randint(min, max)

    def split_cent(self, total, num, min=1):
        """
        RedPackets Split for Cent

        :param total: Total Value of RedPackets
        :param num: Split Num of RedPackets
        :param min: Limit Value of Each Split
        """
        if not (total and num):
            raise ValueError(ZERO_VALUE.format('Num' if total else 'Total'))

        # Convert and Check of Total, Num, Min
        total, num, min = int(total), int(num), int(min)

        # Compare Total and Num * Min
        if total < num * min:
            raise ValueError(TRIPLE_INVALID_VALUE.format(total, num, min))

        split_list = []
        for i in range(1, int(num)):
            # Random Safety High Limit Total
            safe_total = (total - (num - i) * min) / (num - i)
            split_val = int(self.split_cent_val(min * 100, int(safe_total * 100)) / 100)
            total -= split_val
            split_list.append(split_val)
        split_list.append(total)

        # Random Disarrange
        random.shuffle(split_list)

        return split_list

    def split(self, total, num, min=None, cent=False):
        """
        RedPackets Split for Dollor or Cent

        :param total: Total Value of RedPackets
        :param num: Split Num of RedPackets
        :param min: Limit Value of Each Split
        :param cent: Split for Dollor or Cent
        """
        return self.split_cent(total, num, min or 1) if cent else self.split_dollor(total, num, min or 0.01)

    def cent(self, dollar, rate=100):
        """
        Exchange Dollar into Cent

        In [1]: 0.07 * 100
        Out[1]: 7.000000000000001

        :param dollar:
        :param rate:
        :return:
        """
        return int(Decimal(str(dollar)) * rate)

    def dollor(self, cent, rate=100):
        """
        Exchange Cent into Dollor

        :param cent:
        :param rate:
        :return:
        """
        return cent / 100


# For backwards compatibility
_global_instance = RedPackets()
split_dollor = _global_instance.split_dollor
split_cent = _global_instance.split_cent
split = _global_instance.split
cent = _global_instance.cent
dollor = _global_instance.dollor
