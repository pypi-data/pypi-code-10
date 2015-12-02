""" Tests for challenge117 """
from pemjh.challenge117 import challenge117
import pytest


@pytest.mark.regression
def test_challenge117():
    """ Regression testing challenge117 """
    assert challenge117() == 100808458960497L
