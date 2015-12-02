""" Tests for challenge047 """
from pemjh.challenge047 import challenge047
import pytest


@pytest.mark.regression
def test_challenge047():
    """ Regression testing challenge047 """
    assert challenge047() == 134043
