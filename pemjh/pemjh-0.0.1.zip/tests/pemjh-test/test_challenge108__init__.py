""" Tests for challenge108 """
from pemjh.challenge108 import challenge108
import pytest


@pytest.mark.regression
def test_challenge108():
    """ Regression testing challenge108 """
    assert challenge108() == 180180
