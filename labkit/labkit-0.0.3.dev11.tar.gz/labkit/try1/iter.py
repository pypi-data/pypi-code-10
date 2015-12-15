#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry



from itertools import permutations,combinations,product,chain


l=[[1,2],[2,3],[4]]







print list(product([1,2],[2,3],[4]))

print list(apply(product,l))

