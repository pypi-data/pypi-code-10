""" Tests for challenge133 """
from pemjh.challenge133 import challenge133
import pytest


@pytest.mark.regression
def test_challenge133():
    """ Regression testing challenge133 """
    assert challenge133() == 453647705
