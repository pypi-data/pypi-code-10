""" Tests for challenge220 """
from pemjh.challenge220 import challenge220
import pytest


@pytest.mark.regression
def test_challenge220():
    """ Regression testing challenge220 """
    assert challenge220() == '139776,963904'
