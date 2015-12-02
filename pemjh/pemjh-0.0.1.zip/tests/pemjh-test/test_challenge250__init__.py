""" Tests for challenge250 """
from pemjh.challenge250 import challenge250
import pytest


@pytest.mark.regression
def test_challenge250():
    """ Regression testing challenge250 """
    assert challenge250() == 1425480602091519
