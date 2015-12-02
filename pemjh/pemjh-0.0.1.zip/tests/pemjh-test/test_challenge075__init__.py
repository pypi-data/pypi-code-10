""" Tests for challenge075 """
from pemjh.challenge075 import challenge075
import pytest


@pytest.mark.regression
def test_challenge075():
    """ Regression testing challenge075 """
    assert challenge075() == 214954
