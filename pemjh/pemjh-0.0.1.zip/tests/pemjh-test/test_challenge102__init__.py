""" Tests for challenge102 """
from pemjh.challenge102 import challenge102
import pytest


@pytest.mark.regression
def test_challenge102():
    """ Regression testing challenge102 """
    assert challenge102() == 228
