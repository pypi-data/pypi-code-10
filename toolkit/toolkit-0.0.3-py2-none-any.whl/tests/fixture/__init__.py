# coding=utf8

import os
import pytest
from pprint import pprint


@pytest.fixture('session', autouse=True)
def pretty():
    def wrapper(*args):
        print(os.linesep)
        print('-'*60)
        print('Pretty')
        print('-'*60)
        for arg in args:
            pprint(args)
            print('-'*60)
    return wrapper
