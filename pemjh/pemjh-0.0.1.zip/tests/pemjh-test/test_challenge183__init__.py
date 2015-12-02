""" Tests for challenge183 """
from pemjh.challenge183 import challenge183
import pytest


@pytest.mark.regression
def test_challenge183():
    """ Regression testing challenge183 """
    assert challenge183() == 48861552
