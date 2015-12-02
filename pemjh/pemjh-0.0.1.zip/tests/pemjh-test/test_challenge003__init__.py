""" Tests for challenge003 """
from pemjh.challenge003 import challenge003
import pytest


@pytest.mark.regression
def test_challenge003():
    """ Regression testing challenge003 """
    assert challenge003() == 6857
