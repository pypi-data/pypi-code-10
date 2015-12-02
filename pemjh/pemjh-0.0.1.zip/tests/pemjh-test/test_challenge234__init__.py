""" Tests for challenge234 """
from pemjh.challenge234 import challenge234
import pytest


@pytest.mark.regression
def test_challenge234():
    """ Regression testing challenge234 """
    assert challenge234() == 1259187438574927161
