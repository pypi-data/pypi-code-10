""" Tests for challenge214 """
from pemjh.challenge214 import challenge214
import pytest


@pytest.mark.regression
def test_challenge214():
    """ Regression testing challenge214 """
    assert challenge214() == 1677366278943
