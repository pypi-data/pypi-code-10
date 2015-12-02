""" Tests for challenge098 """
from pemjh.challenge098 import challenge098
import pytest


@pytest.mark.regression
def test_challenge098():
    """ Regression testing challenge098 """
    assert challenge098() == 18769
