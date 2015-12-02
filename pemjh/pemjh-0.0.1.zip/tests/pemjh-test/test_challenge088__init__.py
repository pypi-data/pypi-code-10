""" Tests for challenge088 """
from pemjh.challenge088 import challenge088
import pytest


@pytest.mark.regression
def test_challenge088():
    """ Regression testing challenge088 """
    assert challenge088() == 7587457
