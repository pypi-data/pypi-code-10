""" Tests for challenge146 """
from pemjh.challenge146 import challenge146
import pytest


@pytest.mark.regression
def test_challenge146():
    """ Regression testing challenge146 """
    assert challenge146() == 676333270
