""" Tests for challenge094 """
from pemjh.challenge094 import challenge094
import pytest


@pytest.mark.regression
def test_challenge094():
    """ Regression testing challenge094 """
    assert challenge094() == 518408346
