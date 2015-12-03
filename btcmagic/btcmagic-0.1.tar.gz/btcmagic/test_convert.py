from unittest import TestCase
from btcmagic import convert

class TestBase58Check(TestCase):

    def test_b58(self):
        vectors = [
            ("", ""),
            ("61", "2g"),
            ("626262", "a3gV"),
            ("636363", "aPEr"),
            ("73696d706c792061206c6f6e6720737472696e67", "2cFupjhnEsSn59qHXstmK2ffpLv2"),
            ("00eb15231dfceb60925886b67d065299925915aeb172c06647", "1NS17iag9jJgTHD1VXjvLCEnZuQ3rJDE9L"),
            ("516b6fcd0f", "ABnLTmg"),
            ("bf4f89001e670274dd", "3SEo3LWLoPntC"),
            ("572e4794", "3EFU7m"),
            ("ecac89cad93923c02321", "EJDM8drfXA6uyA"),
            ("10c8511e", "Rt5zm"),
            ("00000000000000000000", "1111111111")
        ]

        for v in vectors:
            self.assertEqual(
                convert.bytes_to_b58(convert.hex_to_bytes(v[0])),
                v[1]
            )
            self.assertEqual(
                convert.b58_to_bytes(v[1]),
                convert.hex_to_bytes(v[0])
            )

    def test_b58check(self):
        vectors = [
            ('', '3QJmnh'),
            ('61', 'C2dGTwc'),
            ('626262', '4jF5uERJAK'),
            ('636363', '4mT4krqUYJ'),
            ('73696d706c792061206c6f6e6720737472696e67', 'BXF1HuEUCqeVzZdrKeJjG74rjeXxqJ7dW'),
            ('00eb15231dfceb60925886b67d065299925915aeb172c06647', '13REmUhe2ckUKy1FvM7AMCdtyYq831yxM3QeyEu4'),
            ('516b6fcd0f', '237LSrY9NUUas'),
            ('bf4f89001e670274dd', 'GwDDDeduj1jpykc27e'),
            ('572e4794', 'FamExfqCeza'),
            ('ecac89cad93923c02321', '2W1Yd5Zu6WGyKVtHGMrH'),
            ('10c8511e', '3op3iuGMmhs'),
            ('00000000000000000000', '111111111146Momb')
        ]

        for v in vectors:
            self.assertEqual(
                convert.bytes_to_b58check(convert.hex_to_bytes(v[0])),
                v[1]
            )
            self.assertEqual(
                convert.b58check_to_bytes(v[1]),
                convert.hex_to_bytes(v[0])
            )
