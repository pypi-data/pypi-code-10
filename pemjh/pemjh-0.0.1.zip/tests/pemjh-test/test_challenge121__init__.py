""" Tests for challenge121 """
from pemjh.challenge121 import challenge121
import pytest


@pytest.mark.regression
def test_challenge121():
    """ Regression testing challenge121 """
    assert challenge121() == 2269L
