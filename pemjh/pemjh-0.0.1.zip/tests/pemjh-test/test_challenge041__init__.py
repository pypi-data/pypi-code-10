""" Tests for challenge041 """
from pemjh.challenge041 import challenge041
import pytest


@pytest.mark.regression
def test_challenge041():
    """ Regression testing challenge041 """
    assert challenge041() == 7652413
