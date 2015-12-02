""" Tests for challenge083 """
from pemjh.challenge083 import challenge083
import pytest


@pytest.mark.regression
def test_challenge083():
    """ Regression testing challenge083 """
    assert challenge083() == 425185
