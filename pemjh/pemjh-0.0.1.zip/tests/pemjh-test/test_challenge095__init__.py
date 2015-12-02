""" Tests for challenge095 """
from pemjh.challenge095 import challenge095
import pytest


@pytest.mark.regression
def test_challenge095():
    """ Regression testing challenge095 """
    assert challenge095() == 14316
