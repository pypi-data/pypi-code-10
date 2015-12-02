""" Tests for challenge061 """
from pemjh.challenge061 import challenge061
import pytest


@pytest.mark.regression
def test_challenge061():
    """ Regression testing challenge061 """
    assert challenge061() == 28684
