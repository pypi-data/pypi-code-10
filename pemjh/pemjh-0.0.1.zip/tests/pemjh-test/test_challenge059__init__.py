""" Tests for challenge059 """
from pemjh.challenge059 import challenge059
import pytest


@pytest.mark.regression
def test_challenge059():
    """ Regression testing challenge059 """
    assert challenge059() == 107359
