""" Tests for challenge174 """
from pemjh.challenge174 import challenge174
import pytest


@pytest.mark.regression
def test_challenge174():
    """ Regression testing challenge174 """
    assert challenge174() == 209566
