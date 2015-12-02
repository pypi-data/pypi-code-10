""" Tests for challenge057 """
from pemjh.challenge057 import challenge057
import pytest


@pytest.mark.regression
def test_challenge057():
    """ Regression testing challenge057 """
    assert challenge057() == 153
