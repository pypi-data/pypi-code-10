""" Tests for challenge036 """
from pemjh.challenge036 import challenge036
import pytest


@pytest.mark.regression
def test_challenge036():
    """ Regression testing challenge036 """
    assert challenge036() == 872187
