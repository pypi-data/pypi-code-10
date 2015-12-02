""" Tests for challenge142 """
from pemjh.challenge142 import challenge142
import pytest


@pytest.mark.regression
def test_challenge142():
    """ Regression testing challenge142 """
    assert challenge142() == 1006193
