#!/usr/bin/env python

"""Usage: kaptl init [--backend=mvc] [--frontend=angular] [<rules> | --rules-file=RULESFILE ]
       kaptl edit [ <rules> | --rules-file=RULESFILE ]
       kaptl show
       kaptl -h | --help

Commands:
    init                    Initialize a new application
    edit                    Regenerate an existing application.
                            Requires kaptl_manifest.json to be present in the directory.
    show                    Get information about current project

Arguments:
    <rules>                 Inline string with KAPTL rules. see --rules-file for specifying a path to a file

Options:
    --backend=mvc           Backend framework. Possible values are: "mvc", "sails".
                            If not specified, backend won't be generated
    --frontend=angular      Frontend framework. Possible values are: "angular".
                            If not specified, frontend won't be generated
    --rules-file=RULESFILE  Path to a file with KAPTL rules
    -h, --help              Open this window

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
