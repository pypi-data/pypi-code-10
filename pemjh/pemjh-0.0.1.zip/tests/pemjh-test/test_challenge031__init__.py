""" Tests for challenge031 """
from pemjh.challenge031 import challenge031
import pytest


@pytest.mark.regression
def test_challenge031():
    """ Regression testing challenge031 """
    assert challenge031() == 73682
