""" Tests for challenge026 """
from pemjh.challenge026 import challenge026
import pytest


@pytest.mark.regression
def test_challenge026():
    """ Regression testing challenge026 """
    assert challenge026() == 983
