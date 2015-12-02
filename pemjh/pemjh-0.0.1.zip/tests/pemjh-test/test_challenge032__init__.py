""" Tests for challenge032 """
from pemjh.challenge032 import challenge032
import pytest


@pytest.mark.regression
def test_challenge032():
    """ Regression testing challenge032 """
    assert challenge032() == 45228
