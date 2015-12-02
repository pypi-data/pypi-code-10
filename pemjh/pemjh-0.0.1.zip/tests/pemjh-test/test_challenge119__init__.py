""" Tests for challenge119 """
from pemjh.challenge119 import challenge119
import pytest


@pytest.mark.regression
def test_challenge119():
    """ Regression testing challenge119 """
    assert challenge119() == 248155780267521L
