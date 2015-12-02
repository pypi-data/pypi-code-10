""" Tests for challenge109 """
from pemjh.challenge109 import challenge109
import pytest


@pytest.mark.regression
def test_challenge109():
    """ Regression testing challenge109 """
    assert challenge109() == 38182
