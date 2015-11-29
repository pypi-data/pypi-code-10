# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
from .stats import height_man, height_woman


BOY = 1
GIRL = 2
ERROR = -1.0

BOY_MAX_HEIGHT = 150
GIRL_MAX_HEIGHT = 146


class Baaya(object):
    """
    Intelligent Baaya (Old Wise Lady)

    She answers child age from his/her height.
    Also, she answers child height from his/her age.
    """
    @classmethod
    def age_by_height(cls, height, sex=BOY):
        # guard invalid value
        if sex == BOY and BOY_MAX_HEIGHT <= height:
            return ERROR
        if sex == GIRL and GIRL_MAX_HEIGHT <= height:
            return ERROR

        heights = height_man if sex == BOY else height_woman

        min_age, min_height = min(heights.items())
        if height < min_height:
            return ERROR
        passed_age = min_age
        passed_height = min_height
        for age, height_stats in heights.iteritems():
            if height_stats == height:
                return age
            elif height_stats < height:
                passed_age = age
                passed_height = height_stats
                continue
            else:
                return passed_age + (age - passed_age) * (height - passed_height) / (height_stats - passed_height)

    @classmethod
    def height_by_age(cls, age, sex=BOY):
        heights = height_man if sex == BOY else height_woman

        if age not in heights.keys():
            return ERROR
        else:
            return heights[age]
