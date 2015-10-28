#!/usr/bin/env python

"""Usage: kaptl init [--backend=mvc] --frontend=angular [<rules> | --rules-file=RULESFILE ]
        kaptl edit [ <rules> | --rules-file=RULESFILE ]
        kaptl -h | --help
        kaptl --version

"""

from kaptl import Kaptl
from docopt import docopt


def main():
    args = docopt(__doc__)
    kaptl = Kaptl(args)
    """
    Parse parameters and launch the proper operation
    :type arguments: object
    """
    kaptl.execute_pipeline()


if __name__ == '__main__':
    "Main entry point for KAPTL CLI"
    main()
