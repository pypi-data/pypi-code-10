""" Tests for challenge006 """
from pemjh.challenge006 import challenge006
import pytest


@pytest.mark.regression
def test_challenge006():
    """ Regression testing challenge006 """
    assert challenge006() == 25164150
