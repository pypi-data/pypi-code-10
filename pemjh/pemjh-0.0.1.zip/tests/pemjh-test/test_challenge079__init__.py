""" Tests for challenge079 """
from pemjh.challenge079 import challenge079
import pytest


@pytest.mark.regression
def test_challenge079():
    """ Regression testing challenge079 """
    assert challenge079() == 73162890
