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

from decimal import Decimal

import random


class RedPackets(object):
    def split_val(self, min, max):
        return min if min > max else Decimal(str(random.randint(min, max)))

    def split(self, total, num, min=0.01):
        """
        RedPackets Split & Return split_list if succeed & Raise Exception if failed
        :param total: Total Value of RedPackets
        :param num: Split Num of RedPackets
        :param min: Limit Value of Each Split
        """
        if not (total and num):
            raise ValueError(u'Zero Value of Param {0}'.format('Num' if total else 'Total'))

        # Convert and Check of Total
        total = Decimal(str(total))

        # Convert and Check of Num
        if isinstance(num, float) and int(num) != num:
            raise ValueError(u'Invalid Value for Num: \'{0}\''.format(num))
        num = Decimal(str(int(num)))

        # Convert and Check of Min
        min = Decimal(str(min))

        # Compare Total and Num * Min
        if total < num * min:
            raise ValueError(u'Invalid Value for Total-{0}, Num-{1}, Min-{2}'.format(total, num, min))

        split_list = []
        for i in xrange(1, num):
            # Random Safety High Limit Total
            safe_total = (total - (num - i) * min) / (num - i)
            split_val = self.split_val(min * 100, int(safe_total * 100)) / 100
            total -= split_val
            split_list.append(split_val)
        split_list.append(total)

        # Random Disarrange
        random.shuffle(split_list)

        return split_list

    def cent(self, dollar, rate=100):
        """
        In [1]: 0.07 * 100
        Out[1]: 7.000000000000001
        Exchange Dollar into Cent
        :param dollar:
        :param rate:
        :return:
        """
        return int(Decimal(str(dollar)) * rate)


# For backwards compatibility
_global_instance = RedPackets()
split = _global_instance.split
cent = _global_instance.cent
