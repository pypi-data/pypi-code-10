""" Tests for challenge005 """
from pemjh.challenge005 import challenge005
import pytest


@pytest.mark.regression
def test_challenge005():
    """ Regression testing challenge005 """
    assert challenge005() == 232792560
