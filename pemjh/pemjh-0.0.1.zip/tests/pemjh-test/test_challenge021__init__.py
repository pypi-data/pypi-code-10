""" Tests for challenge021 """
from pemjh.challenge021 import challenge021
import pytest


@pytest.mark.regression
def test_challenge021():
    """ Regression testing challenge021 """
    assert challenge021() == 31626
