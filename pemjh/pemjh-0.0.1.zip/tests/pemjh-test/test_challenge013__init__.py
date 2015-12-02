""" Tests for challenge013 """
from pemjh.challenge013 import challenge013
import pytest


@pytest.mark.regression
def test_challenge013():
    """ Regression testing challenge013 """
    assert challenge013() == 5537376230L
