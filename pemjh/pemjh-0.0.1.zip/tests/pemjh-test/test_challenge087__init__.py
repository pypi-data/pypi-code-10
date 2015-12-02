""" Tests for challenge087 """
from pemjh.challenge087 import challenge087
import pytest


@pytest.mark.regression
def test_challenge087():
    """ Regression testing challenge087 """
    assert challenge087() == 1097343
