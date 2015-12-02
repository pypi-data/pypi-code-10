""" Tests for challenge080 """
from pemjh.challenge080 import challenge080
import pytest


@pytest.mark.regression
def test_challenge080():
    """ Regression testing challenge080 """
    assert challenge080() == 40886
