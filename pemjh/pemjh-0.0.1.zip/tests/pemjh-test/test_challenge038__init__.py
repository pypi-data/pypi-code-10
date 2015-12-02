""" Tests for challenge038 """
from pemjh.challenge038 import challenge038
import pytest


@pytest.mark.regression
def test_challenge038():
    """ Regression testing challenge038 """
    assert challenge038() == 932718654
