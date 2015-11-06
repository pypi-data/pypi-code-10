import unittest
from ..gen import Generator
from ..providers import DefaultProviders


class TestingHelper(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestingHelper, self).__init__(*args, **kwargs)
        self.generator = Generator(provider_list=DefaultProviders)
        self.generator.seed_providers(1)

    def assert_patterns(self, patterns):
        for (pattern, expected) in patterns:
            self.assert_pattern(pattern, expected)

    def assert_pattern(self, pattern, expected):
        result = self.generator.run(pattern)
        assert expected == result
