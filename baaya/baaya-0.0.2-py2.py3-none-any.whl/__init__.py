# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
import optparse
from .baaya import Baaya, BOY, GIRL, ERROR


def main():
    parser = optparse.OptionParser(
        usage='usage: %prog [option]',
        prog='baaya',
        description='Intelligent Baaya (Old Wise Lady)',
    )

    parser.add_option(
        '-s', '--sex',
        help='target sex: {} for BOY, {} for GIRL'.format(BOY, GIRL),
        dest='sex',
        default=BOY,
    )
    parser.add_option(
        '-a', '--age',
        help='Print height by age',
        type='float',
        dest='age',
    )
    parser.add_option(
        '--height',
        help='Print age by height. ',
        type='float',
        dest='height',
    )
    (options, args) = parser.parse_args()

    if options.age is None and options.height is None:
        parser.error('--age or --height should be given')

    if options.age is not None:
        height = Baaya.height_by_age(options.age, options.sex)
        if height == ERROR:
            print("out of scope for age: {}".format(options.age))
        else:
            print("height={} for age={} and sex={}".format(
                height, options.age, options.sex
            ))
    else:
        age = Baaya.age_by_height(options.height, options.sex)
        if age == ERROR:
            print("out of scope for height: {}".format(options.height))
        else:
            print("age={} for height={} and sex={}".format(
                age, options.height, options.sex
            ))
