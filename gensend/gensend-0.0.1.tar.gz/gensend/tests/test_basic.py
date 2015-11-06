from . import TestingHelper


class TestBasic(TestingHelper):
    def test_basic_usage(self):
        patterns = [
            ['%{int}', '4865782901354085937'],
            ['%{IPV4}', '162.241.187.35'],
            ['%{IPV6}', '7ed4:7311:a6ce:c9e9:1807:0741:d5f4:6ec9'],
            ['%{IPCIDR:10.0.0.0/8}', '10.65.76.52'],
            ['%{IPCIDR:2001:db8::/119}', '2001:db8::fd'],
            ['%{IPRANGE:10.1.0.8,10.3.0.1}', '10.1.230.40'],
            ['%{IPRANGE:2001:db8::003f,2001:db8::007f}', '2001:db8::69'],
            ['%{IPGLOB:*.*.*.*}', '201.233.198.6'],
        ]

        for pattern in patterns:
            self.assert_pattern(pattern[0], pattern[1])

    def test_basic_faker(self):
        patterns = [
            ['%{name}', 'Sammie Runolfsdottir'],
            ['%{country}', 'Ecuador'],
        ]

        for pattern in patterns:
            self.assert_pattern(pattern[0], pattern[1])
