#!/usr/bin/python
import argparse
import subprocess
from base64 import b64encode
from passlib.utils.pbkdf2 import pbkdf2


def positive_integer(i):
    try:
        n = int(i)
        if n > 0:
            return n
        else:
            raise ValueError
    except ValueError:
        raise argparse.ArgumentTypeError('invalid positive integer value: '
                                         "'%s'" % i)


def copy(text):
    p = subprocess.Popen(['xclip', '-i'], stdin=subprocess.PIPE)
    p.communicate(text)


def main():
    parser = argparse.ArgumentParser(description='''Use PBKDF2 from Python's
        passlib to derive a key, given a secret and a salt''')

    parser.add_argument('secret')
    parser.add_argument('salt')
    parser.add_argument('-b', '--begin',
                        help='''define where to start slicing the result (equivalent
                             to result[b:])''',
                        default=0,
                        type=int)
    parser.add_argument('-e', '--end',
                        help='''define where to stop slicing the result (equivalent
                             to result[:e])''',
                        type=int)
    parser.add_argument('-f', '--family',
                        help='choose a pseudo-random family',
                        default='sha512',
                        choices=['md5', 'sha1', 'sha256', 'sha512'])
    parser.add_argument('-r', '--rounds',
                        help='''define the number of rounds to use on the generation
                             (an integer greater than zero)''',
                        default=10000,
                        type=positive_integer)
    parser.add_argument('-c', '--copy',
                        help='''copy the output to the clipboard by piping it to
                             xclip instead of printing''',
                        action='store_true')

    args = parser.parse_args()

    result = b64encode(pbkdf2(args.secret, args.salt, args.rounds,
                              prf='hmac-'+args.family))

    if args.end:
        result = result[args.begin:args.end]
    else:
        result = result[args.begin:]

    if args.copy:
        copy(result)
    else:
        print result


if __name__ == '__main__':
    main()
