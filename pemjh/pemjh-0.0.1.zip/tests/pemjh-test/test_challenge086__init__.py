""" Tests for challenge086 """
from pemjh.challenge086 import challenge086
import pytest


@pytest.mark.regression
def test_challenge086():
    """ Regression testing challenge086 """
    assert challenge086() == 1818
