""" Tests for challenge055 """
from pemjh.challenge055 import challenge055
import pytest


@pytest.mark.regression
def test_challenge055():
    """ Regression testing challenge055 """
    assert challenge055() == 249
