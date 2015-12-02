""" Tests for challenge078 """
from pemjh.challenge078 import challenge078
import pytest


@pytest.mark.regression
def test_challenge078():
    """ Regression testing challenge078 """
    assert challenge078() == 55374
