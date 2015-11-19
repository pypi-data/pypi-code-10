import sys
import argparse
from .base import generate_word


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("amount", type=str,
                        help="Amount to convert in string")
    args = parser.parse_args(sys.argv[1:])
    print generate_word(args.amount)
