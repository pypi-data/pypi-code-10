""" Tests for challenge235 """
from pemjh.challenge235 import challenge235
import pytest


@pytest.mark.regression
def test_challenge235():
    """ Regression testing challenge235 """
    assert challenge235() == '1.002322108633'
