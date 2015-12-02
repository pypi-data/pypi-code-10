""" Tests for challenge216 """
from pemjh.challenge216 import challenge216
import pytest


@pytest.mark.regression
def test_challenge216():
    """ Regression testing challenge216 """
    assert challenge216() == 5437849
