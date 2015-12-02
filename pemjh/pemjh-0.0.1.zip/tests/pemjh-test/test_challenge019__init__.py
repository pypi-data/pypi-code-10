""" Tests for challenge019 """
from pemjh.challenge019 import challenge019
import pytest


@pytest.mark.regression
def test_challenge019():
    """ Regression testing challenge019 """
    assert challenge019() == 171
