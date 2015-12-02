""" Tests for challenge203 """
from pemjh.challenge203 import challenge203
import pytest


@pytest.mark.regression
def test_challenge203():
    """ Regression testing challenge203 """
    assert challenge203() == 34029210557338L
