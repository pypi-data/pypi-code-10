""" Tests for challenge053 """
from pemjh.challenge053 import challenge053
import pytest


@pytest.mark.regression
def test_challenge053():
    """ Regression testing challenge053 """
    assert challenge053() == 4075
