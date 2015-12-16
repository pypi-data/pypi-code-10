import codecs
import binascii
import itertools
import re

class binEncoder:
    @staticmethod
    def encode(input, errors=None):
        return ''.join("{:08b}".format(ord(c)) for c in input), len(input)


    @staticmethod
    def decode(input, errors=None):
        #input_iter= iter(input)
        return ''.join(chr(int(''.join(x),2)) for x in filter(lambda x: len(x)==8,re.split('(.{8})',input)))\
                , len(input) & ~7

    class incEncoder:
        def encode(input, final=False):
            return binEncoder.encode(input)

        def reset():
            pass

    class incDecoder:
        def decode(input, final=False):
            return binEncoder.decode(input)

        def reset():
            pass

def wSearcher(name):
    if name=="bin":
        return codecs.CodecInfo(name="bin",
                encode=binEncoder.encode,
                decode=binEncoder.decode,
                streamreader=None,
                streamwriter=None,
                incrementalencoder=binEncoder.incEncoder(),
                incrementaldecoder=binEncoder.incDecoder())

codecs.register(wSearcher)
