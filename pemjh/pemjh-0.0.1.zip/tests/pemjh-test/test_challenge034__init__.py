""" Tests for challenge034 """
from pemjh.challenge034 import challenge034
import pytest


@pytest.mark.regression
def test_challenge034():
    """ Regression testing challenge034 """
    assert challenge034() == 40730
